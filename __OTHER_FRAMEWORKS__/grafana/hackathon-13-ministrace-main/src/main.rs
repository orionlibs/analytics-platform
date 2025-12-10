use clap::Parser;
use nix::{
    errno::Errno,
    sys::{ptrace, signal, wait},
    unistd::{self, Pid},
};
use std::{
    ffi::{CStr, CString, OsString},
    process,
};
use tracing::{error, info, warn};
use tracing_subscriber::layer::SubscriberExt;

#[cfg(not(target_os = "linux"))]
compile_error!("ministrace is only supported on Linux");

/// A small, fast, and optinionated strace subset alternative.
///
/// The program uses ptrace to track system calls and events of a child process.
/// There is minimal overhead, only intending to log messages, however ptrace is not free.
/// The tool supports logging with both JSON and logfmt, to either stdout or stderr.
/// The tool does not log with these nicer formats during the setup phase, only starting as the child process is forked and started.
///
/// It is not intended to be a full replacement for strace, but rather a tool for specifically logging execution events in a way that can be easily ingested and used by Loki.
#[derive(Debug, Parser)]
#[command(name = "ministrace", version, about)]
// TODO: Would be nice to list the authors.
#[command(long_version = concat!(clap::crate_version!(), "\nCopyright (c) 2025 Grafana Labs\n\nThis is free software: you are free to change and redistribute it.\nLicensed under the GNU General Public License v3.0 or later"))]
struct Args {
    /// The duration to wait for all child processes to exit before giving up upon a failure in the ministrace process.
    ///
    /// After this timeout, the child processes will be sent SIGKILL signals.
    #[arg(
        short = 't',
        long,
        default_value = "20s",
        env = "MINISTRACE_FAILURE_TIMEOUT"
    )]
    failure_timeout: humantime::Duration,

    /// Whether to log in JSON format instead of the default logfmt format.
    #[arg(short, long, env = "MINISTRACE_JSON")]
    json: bool,

    /// Whether to ignore new processes.
    #[arg(long, env = "MINISTRACE_IGNORE_NEW_PROCESSES")]
    ignore_new_processes: bool,

    /// Whether to ignore when processes exit or are signaled.
    #[arg(long, env = "MINISTRACE_IGNORE_EXITED_PROCESSES")]
    ignore_exited_processes: bool,

    /// Whether to ignore executed commands.
    #[arg(long, env = "MINISTRACE_IGNORE_EXECUTED_COMMANDS")]
    ignore_executed_commands: bool,

    /// Whether to ignore seccomp events.
    #[arg(long, env = "MINISTRACE_IGNORE_SECCOMP_EVENTS")]
    ignore_seccomp_events: bool,

    /// Whether to ignore ptrace syscall events.
    #[arg(long, env = "MINISTRACE_IGNORE_SYSCALLS")]
    ignore_syscalls: bool,

    /// Whether to ignore unknown wait statuses.
    #[arg(long, env = "MINISTRACE_IGNORE_UNKNOWN_STATUSES")]
    ignore_unknown_statuses: bool,

    /// Whether to ignore unknown ptrace events.
    #[arg(long, env = "MINISTRACE_IGNORE_UNKNOWN_EVENTS")]
    ignore_unknown_events: bool,

    /// The command to trace. Usually a path to an executable, but PATH will also be searched.
    #[arg(required = true, value_name = "COMMAND", env = "MINISTRACE_COMMAND")]
    command: OsString,

    /// The arguments to the command to trace. If not specified, the command will be run without any arguments.
    ///
    /// The command will receive the COMMAND argument as its first argument, as is standard on Linux.
    #[arg(required = false, num_args = 0.., value_name = "ARGS", env = "MINISTRACE_COMMAND_ARGS")]
    command_args: Vec<OsString>,
}

fn main() {
    // The main function should not run any background tasks or similar until after we have forked (as then we are the parent process).
    //   (what is forking? see `man 2 fork`)
    // This is to avoid calling malloc or similar in the child process, which is not async-signal-safe.
    //   (what is async-signal-safe? see `man 7 signal-safety`)
    // Before the fork, we are free to allocate memory and whatnot, however, so it is only AFTER the fork we should be careful.

    let args = Args::parse();

    // We prepare all the inputs to the child process before forking, such that it is in the copied memory space of both processes.
    let Ok(command) = CString::new(args.command.as_encoded_bytes()) else {
        eprintln!(
            "ministrace: invalid command name (contains a nul byte): {}",
            args.command.to_string_lossy(),
        );
        process::exit(1);
    };
    let Ok(mut command_args) = args
        .command_args
        .iter()
        .map(|arg| CString::new(arg.as_encoded_bytes()))
        .collect::<Result<Vec<CString>, _>>()
    else {
        eprintln!("ministrace: invalid command arguments (a value contains a nul byte)");
        process::exit(1);
    };
    command_args.insert(0, command.clone()); // The first argument is the command itself, as per convention.

    let Some(environ) = copy_environ() else {
        eprintln!("ministrace: failed to copy environment variables");
        process::exit(1);
    };

    // While it's not necessarily required, we make sure the stderr pipe's lock is allocated and ready.
    // This is to ensure that the child process does not attempt to allocate any lock or memory around this.
    //   (why? see `man 7 signal-safety` on why we can't malloc)
    drop(std::hint::black_box(std::io::stderr().lock()));

    // SAFETY: This is safe so long as we adhere to the new restrictions we're imposing on ourselves: the child MUST NOT allocate memory or do anything that is not async-signal-safe.
    // As such, we should avoid calling library functions beyond ::nix so as to be able to trust they will NOT do anything unsafe.
    match unsafe { unistd::fork() } {
        Err(e) => {
            // We're on the parent process side, as no child was created.
            // As such, no restrictions are imposed on us here.
            eprintln!("ministrace: fork failed: {e}");
            process::exit(1);
        }

        Ok(unistd::ForkResult::Child) => child_process(&command, &command_args, &environ),

        Ok(unistd::ForkResult::Parent { child, .. }) => {
            // Set up the logging system now before moving on.
            if args.json {
                tracing_subscriber::fmt().json().init();
            } else {
                let registry = tracing_subscriber::registry().with(tracing_logfmt::layer());
                tracing::dispatcher::set_global_default(tracing::dispatcher::Dispatch::new(
                    registry,
                ))
                .expect("failed to set global default tracing dispatcher");
            }

            // Spin up the worker for the parent process.
            let (main_child_exit_code, children) = match parent_process(child, &args) {
                Ok(exit_code) => exit_code,
                Err(err) => {
                    error!(%err, "parent process failed");
                    (128, 1)
                }
            };
            // ... and if we have nothing to clean up, we just exit.
            if children == 0 {
                process::exit(main_child_exit_code);
            }

            // Clean up is split into 3 parts: immediately SIGINT (aka CTRL-C) all the processes in the group,
            //   then wait for half the timeout duration before sending SIGTERM (aka polite kill) to all processes in the group,
            //   and finally wait for the other half of the timeout duration before sending SIGKILL (aka forceful kill) to all processes in the group.
            // We use the PID group 0 to send signals to all processes in the same group as the main child process. That should only be children.
            //   (see more in `man 2 kill`, `man 2 signal`, and `man 7 signal`)
            match signal::kill(Pid::from_raw(0), signal::SIGINT) {
                Ok(()) => (),
                // ESRCH means no processes received the signal.
                Err(Errno::ESRCH) => process::exit(main_child_exit_code),
                Err(errno) => {
                    warn!(%errno, "failed to send SIGINT to own group");
                }
            }

            let half = args.failure_timeout.as_millis() / 2;
            if half > 0 {
                // Wait for half the timeout duration before sending SIGTERM to the child processes.
                std::thread::sleep(std::time::Duration::from_millis(half as u64));
            }

            match signal::kill(Pid::from_raw(0), signal::SIGTERM) {
                Ok(()) => (),
                Err(Errno::ESRCH) => process::exit(main_child_exit_code),
                Err(errno) => {
                    warn!(%errno, "failed to send SIGTERM to own group");
                }
            }

            if half > 0 {
                // Wait for the other half of the timeout duration before sending SIGKILL to the child processes.
                std::thread::sleep(std::time::Duration::from_millis(half as u64));
            } else {
                std::thread::sleep(args.failure_timeout.into());
            }

            match signal::kill(Pid::from_raw(0), signal::SIGKILL) {
                Ok(()) => (),
                Err(Errno::ESRCH) => (),
                Err(errno) => {
                    error!(%errno, "failed to send SIGKILL to own group");
                }
            }

            process::exit(main_child_exit_code);
        }
    }
}

fn child_process(
    command: &CStr,
    command_args: &[impl AsRef<CStr>],
    environ: &[impl AsRef<CStr>],
) -> ! {
    // This is the child process. We MUST NOT allocate memory here.
    // As such, logs are written by directly accessing the stderr pipe.
    // Stderr is chosen as it is not buffered, whereas stdout is. As such, we can't use stdout at all right here.

    use std::io::Write;
    if let Err(e) = ptrace::traceme() {
        // This could definitely be prettier and in some more "reusable" function, but we do it 3 times, so it's just not worth the effort.
        let mut handle = std::io::stderr().lock();
        let _ = handle.write_all(b"ministrace: traceme failed: ");
        let _ = handle.write_all(e.desc().as_bytes());
        let _ = handle.write(b"\n");
        drop(handle);
        process::exit(1);
    }
    if let Err(e) = signal::raise(signal::SIGSTOP) {
        let mut handle = std::io::stderr().lock();
        let _ = handle.write_all(b"ministrace: raise(SIGSTOP) failed: ");
        let _ = handle.write_all(e.desc().as_bytes());
        let _ = handle.write(b"\n");
        drop(handle);
        process::exit(1);
    }

    // We will unwrap_err this, as if the execvpe call succeeds, we will never move on from it.
    // It replaces the entire process image with the new command, and as such, it's stepping into a function from which we will never return unless it fails.
    let e = unistd::execvpe(command, command_args, environ).unwrap_err();
    let mut handle = std::io::stderr().lock();
    let _ = handle.write_all(b"ministrace: execvpe failed: ");
    let _ = handle.write_all(e.desc().as_bytes());
    let _ = handle.write(b"\n");
    drop(handle);
    process::exit(1);
}

fn parent_process(child: Pid, args: &Args) -> Result<(i32, usize), ParentError> {
    // This is the parent process. The constraints do not apply to us, BUT we cannot drop the memory we have until the children have all exited.
    if !args.ignore_new_processes {
        info!(child_pid = %child, "child process has been created");
    }

    // (see `man 2 ptrace` for the exact option info)
    let options = ptrace::Options::PTRACE_O_TRACEEXEC // man 2 execve
        | ptrace::Options::PTRACE_O_TRACECLONE // man 2 clone
        | ptrace::Options::PTRACE_O_TRACEFORK // man 2 fork
        | ptrace::Options::PTRACE_O_TRACEVFORK // man 2 vfork
        | ptrace::Options::PTRACE_O_TRACESECCOMP; // man 2 seccomp
    ptrace::setoptions(child, options)
        .map_err(|errno| ParentError::PtraceSetOptionsFailed(child, errno))?;

    let mut main_child_exit_code = 0; // to return the same from ministrace
    let mut children = 1usize; // to track whether we need to clean up child processes

    loop {
        // We wait for any child process to change state. As we don't pass WNOHANG, this will just block until a child process changes state.
        // As such, we are not spinlocking here.
        // The children processes will just work like usual until they hit a ptrace trap, at which point they'll either raise a SIGSTOP or a SIGTRAP signal.
        //   (see `man 2 wait`)
        let status = match wait::waitpid(None, None) {
            Ok(status) => status,
            // man 2 wait:
            //   ECHILD (for waitpid() or waitid()) The process specified by pid (waitpid()) or idtype and id (waitid()) does not exist or is not  a  child  of
            //   the  calling process.  (This can happen for one's own child if the action for SIGCHLD is set to SIG_IGN.  See also the Linux Notes sec‐
            //   tion about threads.)
            Err(Errno::ECHILD) => break,
            // man 2 wait:
            //   EINTR  WNOHANG was not set and an unblocked signal or a SIGCHLD was caught; see signal(7).
            Err(Errno::EINTR) => continue,
            Err(errno) => return Err(ParentError::WaitpidFailure(errno)),
        };

        match status {
            wait::WaitStatus::Exited(pid, exit_code) => {
                if !args.ignore_exited_processes {
                    info!(event = "child_exited", %pid, %exit_code, "child process exited");
                }
                children -= 1;
                if pid == child {
                    main_child_exit_code = exit_code;
                }
            }
            wait::WaitStatus::Signaled(pid, signal, was_coredumped) => {
                if !args.ignore_exited_processes {
                    info!(event = "child_signaled", %pid, %signal, was_coredumped, "child process was killed by signal");
                }
                children -= 1;
                if pid == child {
                    main_child_exit_code = 128i32.wrapping_add(signal as _); // Convert signal to exit code
                    if main_child_exit_code == 0 {
                        main_child_exit_code = 128; // If the signal wrapped around to 0, we set it to 128 to indicate non-OK.
                    }
                }
            }

            wait::WaitStatus::Stopped(pid, _) => {
                // The child raised a SIGSTOP signal. We will continue it now that we're attached and got the event.
                if let Err(errno) = ptrace::cont(pid, None) {
                    error!(%errno, %pid, "failed to continue child process after stop");
                }
            }

            wait::WaitStatus::PtraceEvent(pid, signal, event) => {
                if event == ptrace::Event::PTRACE_EVENT_FORK as i32 {
                    children += 1;
                    if !args.ignore_new_processes {
                        match ptrace::getevent(pid) {
                            Ok(new_pid) => {
                                info!(event = "child_forked", %pid, %new_pid, "child process forked");
                            }
                            Err(errno) => {
                                warn!(event = "child_forked", %pid, %errno, "child process forked, but failed to get new PID");
                            }
                        }
                    }
                } else if event == ptrace::Event::PTRACE_EVENT_VFORK as i32 {
                    children += 1;
                    if !args.ignore_new_processes {
                        match ptrace::getevent(pid) {
                            Ok(new_pid) => {
                                info!(event = "child_vforked", %pid, %new_pid, "child process forked");
                            }
                            Err(errno) => {
                                warn!(event = "child_vforked", %pid, %errno, "child process forked, but failed to get new PID");
                            }
                        }
                    }
                } else if event == ptrace::Event::PTRACE_EVENT_CLONE as i32 {
                    children += 1;
                    if !args.ignore_new_processes {
                        match ptrace::getevent(pid) {
                            Ok(new_pid) => {
                                info!(event = "child_cloned", %pid, %new_pid, "child process cloned");
                            }
                            Err(errno) => {
                                warn!(event = "child_cloned", %pid, %errno, "child process cloned, but failed to get new PID");
                            }
                        }
                    }
                } else if event == ptrace::Event::PTRACE_EVENT_EXEC as i32 {
                    if !args.ignore_executed_commands {
                        // The /proc/ pseudo-filesystem is Linux' way to expose process information to the userspace.
                        // They act as real files, despite not being so, and are just a filesystem "format" handled by the kernel.
                        //   (see `man 5 proc` for more)
                        let cmdline =
                            std::fs::read(format!("/proc/{pid}/cmdline")).unwrap_or_default();
                        let cmdline = format_cmdline(cmdline);

                        match std::fs::read_link(format!("/proc/{pid}/exe"))
                            .map(|path| path.to_string_lossy().to_string())
                        {
                            Ok(exe) => {
                                info!(event = "child_exec", %pid, cmdline, exe, "child process executed a new program");
                            }
                            Err(error) => {
                                warn!(event = "child_exec", %pid, cmdline, %error, "child process executed a new program, but failed to read the executable path");
                            }
                        }
                    }
                } else if event == ptrace::Event::PTRACE_EVENT_SECCOMP as i32 {
                    if !args.ignore_syscalls {
                        match ptrace::getevent(pid).map(|data| data as u64) {
                            Ok(ret_data) => {
                                info!(event = "child_seccomp", %pid, ret_data, "child process hit a seccomp filter");
                            }
                            Err(errno) => {
                                warn!(event = "child_seccomp", %pid, %errno, "child process hit a seccomp filter, but failed to get data");
                            }
                        }
                    }
                } else if !args.ignore_unknown_events {
                    info!(event = "child_ptrace_event", %pid, %signal, event = ?event, "child process stopped at ptrace event");
                }

                ptrace::cont(pid, None)
                    .map_err(|errno| ParentError::PtraceContinueFailed(pid, errno))?;
            }
            wait::WaitStatus::PtraceSyscall(pid) => {
                if !args.ignore_syscalls {
                    info!(event = "child_ptrace_syscall", %pid, "child process stopped at syscall");
                }
                ptrace::cont(pid, None)
                    .map_err(|errno| ParentError::PtraceContinueFailed(pid, errno))?;
            }

            otherwise => {
                // This is an unexpected status, just continue waiting.
                if !args.ignore_unknown_statuses {
                    info!(
                        event = "unknown_wait_status",
                        status = ?otherwise,
                        "unknown wait status received"
                    );
                }
            }
        }
    }

    Ok((main_child_exit_code, children))
}

/// The parent process error type.
///
/// This can contain heap references and similar, as the children
#[derive(Debug, thiserror::Error)]
enum ParentError {
    #[error("failed to set ptrace options for child process {0}: {1}")]
    PtraceSetOptionsFailed(Pid, Errno),

    #[error("failed to wait for child process' state change: {0}")]
    WaitpidFailure(Errno),

    #[error("failed to continue stopped child process {0}: {1}")]
    PtraceContinueFailed(Pid, Errno),
}

fn copy_environ() -> Option<Vec<CString>> {
    std::env::vars_os()
        .filter(|(key, _)| !key.to_string_lossy().starts_with("MINISTRACE_"))
        .map(|(key, value)| {
            let joined = key
                .as_encoded_bytes()
                .iter()
                .chain(b"=")
                .chain(value.as_encoded_bytes())
                .cloned()
                .collect::<Vec<_>>();
            CString::new(joined)
        })
        .collect::<Result<Vec<_>, _>>()
        .ok()
}

fn format_cmdline(cmdline: Vec<u8>) -> String {
    // The cmdline is a string with arguments separated by nul bytes.
    use shell_quote::Bash;
    let cmdline = cmdline
        .split_inclusive(|&b| b == 0)
        // from_bytes_with_nul is fine as we include the nul with split_inclusive.
        .filter_map(|s| CStr::from_bytes_with_nul(s).ok())
        .map(|s| s.to_string_lossy().into_owned())
        .map(|s| {
            // We need to escape the command line arguments, as they may contain spaces and other special characters.
            // Bash::quote_vec will handle this for us.
            Bash::quote_vec(&s)
        })
        .collect::<Vec<_>>();
    let joined = cmdline.join(&b' ');
    String::from_utf8_lossy(&joined).into()
}

#[cfg(test)]
mod tests {
    use clap::CommandFactory;

    #[test]
    fn clap_valid() {
        super::Args::command().debug_assert();
    }
}

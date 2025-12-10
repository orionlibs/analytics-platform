# ministrace ![](https://img.shields.io/badge/license-GPL--3.0--Or--Later-blue) ![](https://img.shields.io/badge/written--in-rust-indianred)

This tool uses [ptrace] to get events about a child process it spawns. It will then log them to stderr in (nd)JSON or logfmt formats.

`strace` is incredibly verbose and does not use a structured, filterable format. As such, we have to either make a parser and make it output (nd)JSON or logfmt ourselves... or we write a replacement.
As this was conceived during an internal hackathon, it seemed more interesting to write a replacement.

[ptrace]: https://man7.org/linux/man-pages/man2/ptrace.2.html

## Maintenance

This is not an official product of Grafana Labs, nor is it maintained as such. Do not expect any support on this project.

If a Grafana Labs employee wishes to productionise this, please feel free.

## References

You may be interested in these references to understand how this application works:

 * [`ptrace(2)`](https://man.archlinux.org/man/core/man-pages/ptrace.2.en)
 * [`execve(2)`](https://man.archlinux.org/man/execve.2)
 * [`fork(2)`](https://man.archlinux.org/man/fork.2)
 * [`vfork(2)`](https://man.archlinux.org/man/vfork.2)
 * [`signal-safety(7)`](https://man.archlinux.org/man/signal-safety.7)
 * [`proc(5)`](https://man.archlinux.org/man/core/man-pages/proc.5.en)
 * [`kill(2)`](https://man.archlinux.org/man/core/man-pages/kill.2.en)
 * [`signal(2)`](https://man.archlinux.org/man/core/man-pages/signal.2.en)
 * [`signal(7)`](https://man.archlinux.org/man/core/man-pages/signal.7.en)
 * [`seccomp(2)`](https://man.archlinux.org/man/seccomp.2)
 * [`clone(2)`](https://man.archlinux.org/man/core/man-pages/clone.2.en)
 * [`wait(2)`](https://man.archlinux.org/man/wait.2)

## License

This project is licensed under the GNU GPLv3 license ("GPL-3.0-only" SPDX identifier).

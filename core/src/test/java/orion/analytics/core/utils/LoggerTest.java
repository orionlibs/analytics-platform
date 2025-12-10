package orion.analytics.core.utils;

import static org.assertj.core.api.Assertions.assertThat;

import nl.altindag.log.LogCaptor;
import org.junit.jupiter.api.Test;

public class LoggerTest
{
    @Test
    void info_logs_message_and_parameters()
    {
        LogCaptor captor = LogCaptor.forClass(Logger.class);
        Logger.info("Hello {}", "world");
        assertThat(captor.getInfoLogs()).hasSize(1);
        assertThat(captor.getInfoLogs().get(0)).isEqualTo("Hello world");
    }


    @Test
    void warning_logs_message_and_parameters()
    {
        LogCaptor captor = LogCaptor.forClass(Logger.class);
        Logger.warning("Low disk: {}%", 15);
        assertThat(captor.getWarnLogs()).hasSize(1);
        assertThat(captor.getWarnLogs().get(0)).isEqualTo("Low disk: 15%");
    }


    @Test
    void error_logs_message_and_parameters()
    {
        LogCaptor captor = LogCaptor.forClass(Logger.class);
        Logger.error("Failure on {}", "node-7");
        assertThat(captor.getErrorLogs()).hasSize(1);
        assertThat(captor.getErrorLogs().get(0)).isEqualTo("Failure on node-7");
    }
}

package orion.analytics.core.trace;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;

public class TraceIDGeneratorTest
{
    private final TraceIDGenerator generator = new TraceIDGenerator();
    private String originalThreadName;


    @BeforeEach
    void setUp()
    {
        originalThreadName = Thread.currentThread().getName();
        MDC.remove("traceID");
    }


    @AfterEach
    void tearDown()
    {
        MDC.remove("traceID");
        Thread.currentThread().setName(originalThreadName);
    }


    @Test
    void generateTraceID_returnsValidUuid_andSetsMdcAndThreadName()
    {
        String traceId = generator.generateTraceID();
        assertThat(traceId).isNotNull();
        UUID parsed = UUID.fromString(traceId);
        assertThat(parsed).isNotNull();
        assertThat(MDC.get("traceID")).isEqualTo(traceId);
        assertThat(Thread.currentThread().getName()).isEqualTo(traceId);
    }


    @Test
    void generateTraceID_producesDifferentValues_onConsecutiveCalls_andUpdatesMdcAndThreadName()
    {
        String first = generator.generateTraceID();
        String second = generator.generateTraceID();
        assertThat(UUID.fromString(first)).isNotNull();
        assertThat(UUID.fromString(second)).isNotNull();
        assertThat(first).isNotEqualTo(second);
        assertThat(MDC.get("traceID")).isEqualTo(second);
        assertThat(Thread.currentThread().getName()).isEqualTo(second);
    }
}

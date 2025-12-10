package orion.analytics.core.trace;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

public class TraceServiceTest
{
    private AnnotationConfigApplicationContext context;
    private String originalThreadName;


    @BeforeEach
    void setUp()
    {
        originalThreadName = Thread.currentThread().getName();
        MDC.remove("traceID");
        context = new AnnotationConfigApplicationContext(Config.class);
    }


    @AfterEach
    void tearDown()
    {
        context.close();
        MDC.remove("traceID");
        Thread.currentThread().setName(originalThreadName);
    }


    @Test
    void generateTraceID_viaService_returnsValidUuid_andSetsMdcAndThreadName()
    {
        TraceService service = context.getBean(TraceService.class);
        String traceId = service.generateTraceID();
        assertThat(traceId).isNotNull();
        UUID uuid = UUID.fromString(traceId);
        assertThat(uuid).isNotNull();
        assertThat(MDC.get("traceID")).isEqualTo(traceId);
        assertThat(Thread.currentThread().getName()).isEqualTo(traceId);
    }


    @Configuration
    @ComponentScan("orion.analytics.core.trace")
    static class Config
    {
    }
}

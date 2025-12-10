package orion.analytics.core.trace;

import java.util.UUID;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

@Component
class TraceIDGenerator
{
    String generateTraceID()
    {
        String traceID = UUID.randomUUID().toString();
        MDC.put("traceID", traceID);
        Thread.currentThread().setName(traceID);
        return traceID;
    }
}

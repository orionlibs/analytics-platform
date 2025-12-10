package orion.analytics.core.trace;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TraceService
{
    @Autowired private TraceIDGenerator traceIDGenerator;


    public String generateTraceID()
    {
        return traceIDGenerator.generateTraceID();
    }
}

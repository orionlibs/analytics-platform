package orion.analytics.core.api.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import orion.analytics.core.trace.TraceService;

@Component
public class TraceFilter extends OncePerRequestFilter
{
    @Autowired private TraceService traceService;


    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException
    {
        traceService.generateTraceID();
        filterChain.doFilter(request, response);
    }
}

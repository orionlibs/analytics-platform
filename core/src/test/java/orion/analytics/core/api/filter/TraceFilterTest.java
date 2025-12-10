package orion.analytics.core.api.filter;

import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import orion.analytics.core.trace.TraceService;
import orion.analytics.core.utils.ReflectionUtils;

public class TraceFilterTest
{
    private TraceFilter traceFilter;
    private TraceService traceService;
    private HttpServletRequest request;
    private HttpServletResponse response;
    private FilterChain filterChain;


    @BeforeEach
    void setUp()
    {
        traceFilter = new TraceFilter();
        traceService = mock(TraceService.class);
        request = mock(HttpServletRequest.class);
        response = mock(HttpServletResponse.class);
        filterChain = mock(FilterChain.class);
        ReflectionUtils.injectObject(traceFilter, "traceService", traceService);
    }


    @Test
    void doFilterInternal_callsGenerateTraceID_andDelegatesToFilterChain() throws ServletException, IOException
    {
        traceFilter.doFilterInternal(request, response, filterChain);
        verify(traceService, times(1)).generateTraceID();
        verify(filterChain, times(1)).doFilter(request, response);
    }


    @Test
    void doFilterInternal_callsGenerateTraceID_evenIfExceptionInChain() throws IOException, ServletException
    {
        doThrow(new IOException("Chain error")).when(filterChain).doFilter(request, response);
        try
        {
            traceFilter.doFilterInternal(request, response, filterChain);
        }
        catch(IOException e)
        {
            // expected
        }
        verify(traceService, times(1)).generateTraceID();
        verify(filterChain, times(1)).doFilter(request, response);
    }
}

package orion.analytics.core.test;

import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;

@Component
class TestHTTPHeader
{
    HttpHeaders getHttpHeaders(HttpHeaders headers)
    {
        if(headers == null)
        {
            return new HttpHeaders();
        }
        return headers;
    }
}

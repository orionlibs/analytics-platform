package orion.analytics.app;

import org.springframework.stereotype.Component;

@Component
public class TestBase
{
    protected String apiEndpointPrefix = "http://localhost:";


    protected void addPortToAPIEndpoint(int port)
    {
        this.apiEndpointPrefix += port;
    }
}

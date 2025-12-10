package orion.analytics.app.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "orion")
@Data
public class Config
{
    private String bitbucketApiToken;


    @Data
    public static class Class1
    {
        private String token;
    }
}

package orion.analytics.app.configuration;

import java.util.Properties;
import org.springframework.beans.factory.config.YamlPropertiesFactoryBean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;

@Configuration
public class SpringConfiguration
{
    public SpringConfiguration()
    {
        loadConfiguration();
    }


    public void loadConfiguration()
    {
        YamlPropertiesFactoryBean yamlFactory = new YamlPropertiesFactoryBean();
        yamlFactory.setResources(new ClassPathResource("application.yml"));
        Properties allProperties = yamlFactory.getObject();
        if(allProperties != null)
        {
            allProperties.forEach((key, value) -> {
                String k = key.toString();
                if(k.startsWith("orion."))
                {
                    orion.analytics.core.configuration.Configuration.addProp(k, value);
                }
            });
        }
    }
}
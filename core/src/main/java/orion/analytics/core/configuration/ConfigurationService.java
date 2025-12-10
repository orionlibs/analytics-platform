package orion.analytics.core.configuration;

import java.io.IOException;
import java.io.InputStream;

public class ConfigurationService
{
    public static void loadConfigurationFromFile(InputStream configurationFile) throws IOException
    {
        Configuration.addProps(configurationFile);
    }
}

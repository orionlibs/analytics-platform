package orion.analytics.core.configuration;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class Configuration extends Properties
{
    private static final Properties PROPERTIES;

    static
    {
        PROPERTIES = new Properties();
    }

    private Configuration()
    {
    }


    public static void addProp(String key, Object value)
    {
        PROPERTIES.put(key, value);
    }


    public static void addProps(InputStream inputStream) throws IOException
    {
        PROPERTIES.load(inputStream);
    }


    public static Object getProp(String key)
    {
        return PROPERTIES.getProperty(key);
    }


    public static void deleteProp(String key)
    {
        PROPERTIES.remove(key);
    }
}

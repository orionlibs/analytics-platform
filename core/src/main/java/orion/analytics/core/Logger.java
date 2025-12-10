package orion.analytics.core;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Logger
{
    private Logger()
    {
    }


    public static void info(String message, Object... parameters)
    {
        log.info(message, parameters);
    }


    public static void warning(String message, Object... parameters)
    {
        log.warn(message, parameters);
    }


    public static void error(String message, Object... parameters)
    {
        log.error(message, parameters);
    }
}

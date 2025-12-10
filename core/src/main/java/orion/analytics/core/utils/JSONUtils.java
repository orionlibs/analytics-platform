package orion.analytics.core.utils;

import tools.jackson.core.JacksonException;
import tools.jackson.databind.ObjectMapper;
import tools.jackson.databind.SerializationFeature;
import tools.jackson.databind.cfg.DateTimeFeature;
import tools.jackson.databind.json.JsonMapper;

public final class JSONUtils
{
    private static ObjectMapper mapper;

    static
    {
        mapper = JsonMapper.builder()
                        //.propertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE)
                        .enable(SerializationFeature.FAIL_ON_EMPTY_BEANS, SerializationFeature.FAIL_ON_SELF_REFERENCES)
                        .enable(DateTimeFeature.WRITE_DATES_AS_TIMESTAMPS)
                        .build();
    }

    private JSONUtils()
    {
    }


    public static String convertObjectToJSON(Object objectToConvert)
    {
        try
        {
            return mapper.writeValueAsString(objectToConvert);
        }
        catch(JacksonException e)
        {
            return "";
        }
    }


    public static Object convertJSONToObject(String jsonData, Class<?> classToConvertTo) throws JacksonException
    {
        return mapper.readValue(jsonData, classToConvertTo);
    }
}

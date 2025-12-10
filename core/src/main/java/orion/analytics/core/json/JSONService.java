package orion.analytics.core.json;

import tools.jackson.core.JacksonException;

public final class JSONService
{
    private JSONService()
    {
    }


    public static String convertObjectToJSON(Object objectToConvert)
    {
        try
        {
            return JSONMapper.getMapper().writeValueAsString(objectToConvert);
        }
        catch(JacksonException e)
        {
            return "";
        }
    }


    public static Object convertJSONToObject(String jsonData, Class<?> classToConvertTo) throws JacksonException
    {
        return JSONMapper.getMapper().readValue(jsonData, classToConvertTo);
    }
}

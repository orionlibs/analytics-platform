package orion.analytics.core.utils;

import java.lang.reflect.Field;
import java.util.Collection;

public class ReflectionUtils
{
    public static void injectObject(Object object, String fieldName, Object objectToInject)
    {
        try
        {
            Field field = object.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(object, objectToInject);
        }
        catch(NoSuchFieldException | IllegalAccessException e)
        {
            throw new RuntimeException("Failed to inject TraceService mock", e);
        }
    }


    public static Collection<Object> extractFieldValues(Object obj)
    {
        try
        {
            Field[] fields = obj.getClass().getDeclaredFields();
            java.util.List<Object> values = new java.util.ArrayList<>();
            for(Field f : fields)
            {
                f.setAccessible(true);
                values.add(f.get(obj));
            }
            return values;
        }
        catch(Exception e)
        {
            throw new RuntimeException("Failed to extract field values reflectively", e);
        }
    }
}

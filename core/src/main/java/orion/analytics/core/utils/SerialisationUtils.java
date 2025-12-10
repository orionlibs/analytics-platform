package orion.analytics.core.utils;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

public class SerialisationUtils
{
    public static byte[] serializeToBytes(Serializable obj) throws IOException
    {
        try(ByteArrayOutputStream baos = new ByteArrayOutputStream();
                        ObjectOutputStream oos = new ObjectOutputStream(baos))
        {
            oos.writeObject(obj);
            oos.flush();
            return baos.toByteArray();
        }
    }


    public static Object deserializeFromBytes(byte[] bytes) throws IOException, ClassNotFoundException
    {
        try(ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                        ObjectInputStream ois = new ObjectInputStream(bais))
        {
            return ois.readObject();
        }
    }
}

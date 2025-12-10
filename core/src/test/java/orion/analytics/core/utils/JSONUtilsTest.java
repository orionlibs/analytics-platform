package orion.analytics.core.utils;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import tools.jackson.core.JacksonException;

public class JSONUtilsTest
{
    @Test
    void convertObjectToJSON_serializesSimpleObject()
    {
        TestData data = new TestData("Alice", 30);
        String json = JSONUtils.convertObjectToJSON(data);
        assertThat(json).isNotNull()
                        .contains("\"name\":\"Alice\"")
                        .contains("\"age\":30");
    }


    @Test
    void convertJSONToObject_deserializesCorrectly() throws JacksonException
    {
        String json = "{\"name\":\"Bob\",\"age\":25}";
        Object obj = JSONUtils.convertJSONToObject(json, TestData.class);
        assertThat(obj).isInstanceOf(TestData.class);
        TestData data = (TestData)obj;
        assertThat(data.name).isEqualTo("Bob");
        assertThat(data.age).isEqualTo(25);
    }


    @Test
    void convertObjectToJSON_returnsEmptyString_onSerializationError() throws Exception
    {
        Object obj = new Object()
        {
            public Object self = this;
        };
        String result = JSONUtils.convertObjectToJSON(obj);
        assertThat(result).isEmpty();
    }


    @Test
    void roundTrip_objectToJsonToObject_preservesData() throws JacksonException
    {
        TestData original = new TestData("Charlie", 40);
        String json = JSONUtils.convertObjectToJSON(original);
        Object obj = JSONUtils.convertJSONToObject(json, TestData.class);
        assertThat(obj).isInstanceOf(TestData.class);
        TestData restored = (TestData)obj;
        assertThat(restored.name).isEqualTo(original.name);
        assertThat(restored.age).isEqualTo(original.age);
    }


    @Test
    void convertJSONToObject_throwsJacksonException_onInvalidJson()
    {
        String invalidJson = "{name:\"Alice\", age:30}";
        assertThatThrownBy(() -> JSONUtils.convertJSONToObject(invalidJson, TestData.class))
                        .isInstanceOf(JacksonException.class);
    }


    static class TestData
    {
        public String name;
        public int age;


        public TestData()
        {
        }


        public TestData(String name, int age)
        {
            this.name = name;
            this.age = age;
        }
    }
}

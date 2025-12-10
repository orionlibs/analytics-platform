package orion.analytics.core.configuration;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

public class ConfigurationTest
{
    private static final String TEST_KEY = "orion.version";
    private static final String TEST_VALUE = "0.0.1";


    @AfterEach
    void cleanup()
    {
        Configuration.deleteAllProps();
    }


    @Test
    void addProp_and_getProp_works()
    {
        Configuration.addProp(TEST_KEY, TEST_VALUE);
        Object value = Configuration.getProp(TEST_KEY);
        assertThat(value).isEqualTo(TEST_VALUE);
    }


    @Test
    void getProp_returnsNull_whenKeyDoesNotExist()
    {
        Object value = Configuration.getProp("nonexistent.key");
        assertThat(value).isNull();
    }


    @Test
    void deleteProp_removesProperty()
    {
        Configuration.addProp(TEST_KEY, TEST_VALUE);
        assertThat(Configuration.getProp(TEST_KEY)).isEqualTo(TEST_VALUE);
        Configuration.deleteProp(TEST_KEY);
        assertThat(Configuration.getProp(TEST_KEY)).isNull();
    }


    @Test
    void addProps_loadsFromInputStream() throws IOException
    {
        String propsContent = """
                        orion.version=0.0.2
                        orion.another.key=hello
                        """;
        try(ByteArrayInputStream input = new ByteArrayInputStream(propsContent.getBytes(StandardCharsets.UTF_8)))
        {
            Configuration.addProps(input);
        }
        assertThat(Configuration.getProp("orion.version")).isEqualTo("0.0.2");
        assertThat(Configuration.getProp("orion.another.key")).isEqualTo("hello");
    }


    @Test
    void addProp_canOverwriteExistingValue()
    {
        Configuration.addProp(TEST_KEY, "initial");
        assertThat(Configuration.getProp(TEST_KEY)).isEqualTo("initial");
        Configuration.addProp(TEST_KEY, "updated");
        assertThat(Configuration.getProp(TEST_KEY)).isEqualTo("updated");
    }
}

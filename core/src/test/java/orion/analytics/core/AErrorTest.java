package orion.analytics.core;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;
import orion.analytics.core.utils.SerialisationUtils;

class AErrorTest
{
    @Test
    void noArgsConstructor_and_setters_getters_work()
    {
        AError<String> error = new AError<>();
        assertThat(error.getErrorCode()).isNull();
        assertThat(error.getErrorMessage()).isNull();
        assertThat(error.getError()).isNull();
        error.setErrorCode("NO_ARG");
        error.setErrorMessage("no-arg message");
        error.setError("payload");
        assertThat(error.getErrorCode()).isEqualTo("NO_ARG");
        assertThat(error.getErrorMessage()).isEqualTo("no-arg message");
        assertThat(error.getError()).isEqualTo("payload");
    }


    @Test
    void twoArgConstructor_sets_code_and_message_and_leaves_error_null()
    {
        AError<Object> error = new AError<>("E100", "two-arg message");
        assertThat(error.getErrorCode()).isEqualTo("E100");
        assertThat(error.getErrorMessage()).isEqualTo("two-arg message");
        assertThat(error.getError()).isNull();
    }


    @Test
    void threeArgConstructor_sets_all_fields()
    {
        AError<Integer> error = new AError<>("E200", "three-arg message", 42);
        assertThat(error.getErrorCode()).isEqualTo("E200");
        assertThat(error.getErrorMessage()).isEqualTo("three-arg message");
        assertThat(error.getError()).isEqualTo(42);
    }


    @Test
    void works_with_complex_generic_type()
    {
        List<String> payload = List.of("a", "b", "c");
        AError<List<String>> error = new AError<>("E-GEN", "generic payload", payload);
        assertThat(error.getErrorCode()).isEqualTo("E-GEN");
        assertThat(error.getErrorMessage()).isEqualTo("generic payload");
        assertThat(error.getError()).isSameAs(payload);
    }


    @Test
    void serializable_preserves_state_after_roundtrip() throws Exception
    {
        AError<String> original = new AError<>("SER001", "serialize test", "body");
        byte[] bytes = SerialisationUtils.serializeToBytes(original);
        Object deserialized = SerialisationUtils.deserializeFromBytes(bytes);
        assertThat(deserialized).isInstanceOf(AError.class);
        @SuppressWarnings("unchecked")
        AError<String> restored = (AError<String>)deserialized;
        assertThat(restored.getErrorCode()).isEqualTo(original.getErrorCode());
        assertThat(restored.getErrorMessage()).isEqualTo(original.getErrorMessage());
        assertThat(restored.getError()).isEqualTo(original.getError());
    }


    @Test
    void setters_accept_null_values()
    {
        AError<String> error = new AError<>("C", "M", "payload");
        error.setErrorCode(null);
        error.setErrorMessage(null);
        error.setError(null);
        assertThat(error.getErrorCode()).isNull();
        assertThat(error.getErrorMessage()).isNull();
        assertThat(error.getError()).isNull();
    }
}
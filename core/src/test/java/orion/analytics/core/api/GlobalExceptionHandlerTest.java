package orion.analytics.core.api;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Collection;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BeanPropertyBindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import orion.analytics.core.AError;
import orion.analytics.core.data.DuplicateRecordException;
import orion.analytics.core.data.ResourceNotFoundException;
import orion.analytics.core.utils.ReflectionUtils;

public class GlobalExceptionHandlerTest
{
    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();


    @Test
    void onValidationError_returnsBadRequest_andContainsFieldErrors() throws NoSuchMethodException
    {
        String objectName = "dto";
        BeanPropertyBindingResult bindingResult = new BeanPropertyBindingResult(new Object(), objectName);
        String field = "name";
        String defaultMessage = "must not be blank";
        Object rejectedValue = "bad-value";
        FieldError fe = new FieldError(objectName, field, rejectedValue, false, null, null, defaultMessage);
        bindingResult.addError(fe);
        MethodArgumentNotValidException ex = Mockito.mock(MethodArgumentNotValidException.class);
        Mockito.when(ex.getBindingResult()).thenReturn(bindingResult);
        ResponseEntity<APIResponse> resp = handler.onValidationError(ex);
        assertThat(resp).isNotNull();
        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.BAD_REQUEST);
        APIResponse body = resp.getBody();
        assertThat(body).isNotNull();
        @SuppressWarnings("unchecked")
        AError<List<Object>> error = (AError<List<Object>>)body.getError();
        assertThat(error).isNotNull();
        assertThat(error.getErrorMessage()).isEqualTo("Validation failed for one or more fields");
        List<?> apiFields = error.getError();
        assertThat(apiFields).isNotNull().hasSize(1);
        Object apiField = apiFields.get(0);
        Collection<Object> values = ReflectionUtils.extractFieldValues(apiField);
        assertThat(values).contains(field, defaultMessage, rejectedValue);
    }


    @Test
    void onDuplicateRecordException_returnsConflict_andMessageContainsCause()
    {
        String causeMessage = "user with id 123 already exists";
        DuplicateRecordException ex = new DuplicateRecordException(causeMessage);
        ResponseEntity<APIResponse> resp = handler.onDuplicateRecordException(ex);
        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.CONFLICT);
        APIResponse body = resp.getBody();
        assertThat(body).isNotNull();
        @SuppressWarnings("rawtypes")
        AError error = body.getError();
        assertThat(error.getErrorMessage()).isEqualTo("Duplicate database record found: " + causeMessage);
    }


    @Test
    void onResourceNotFoundException_returnsNotFound_andMessageContainsResource()
    {
        String causeMessage = "user/42";
        ResourceNotFoundException ex = new ResourceNotFoundException(causeMessage);
        ResponseEntity<APIResponse> resp = handler.onResourceNotFoundException(ex);
        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
        APIResponse body = resp.getBody();
        assertThat(body).isNotNull();
        @SuppressWarnings("rawtypes")
        AError error = body.getError();
        assertThat(error.getErrorMessage()).isEqualTo("Resource not found: " + causeMessage);
    }


    @Test
    void handleIdempotencyConflict_returnsUnprocessableEntity()
    {
        IdempotencyConflictException ex = Mockito.mock(IdempotencyConflictException.class);
        ResponseEntity<APIResponse> resp = handler.handleIdempotencyConflict(ex);
        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.UNPROCESSABLE_ENTITY);
        APIResponse body = resp.getBody();
        assertThat(body).isNotNull();
        @SuppressWarnings("rawtypes")
        AError error = body.getError();
        assertThat(error.getErrorMessage()).isEqualTo("Idempotency conflict");
    }


    @Test
    void handleAllCheckedExceptions_returnsInternalServerError()
    {
        Throwable t = new RuntimeException("boom");
        ResponseEntity<APIResponse> resp = handler.handleAllCheckedExceptions(t);
        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR);
        APIResponse body = resp.getBody();
        assertThat(body).isNotNull();
        @SuppressWarnings("rawtypes")
        AError error = body.getError();
        assertThat(error.getErrorMessage()).isEqualTo("An unexpected error occurred");
    }
}

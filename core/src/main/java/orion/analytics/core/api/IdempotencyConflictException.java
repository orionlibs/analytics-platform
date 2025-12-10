package orion.analytics.core.api;

import orion.analytics.core.exception.UncheckedException;

public class IdempotencyConflictException extends UncheckedException
{
    private static final String DEFAULT_ERROR_MESSAGE = "There was an error.";


    public IdempotencyConflictException(String errorMessage)
    {
        super(errorMessage);
    }


    public IdempotencyConflictException(String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments));
    }


    public IdempotencyConflictException(Throwable cause, String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments), cause);
    }


    public IdempotencyConflictException(Throwable cause)
    {
        super(DEFAULT_ERROR_MESSAGE, cause);
    }
}

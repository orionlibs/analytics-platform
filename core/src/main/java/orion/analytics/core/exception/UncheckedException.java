package orion.analytics.core.exception;

public class UncheckedException extends RuntimeException
{
    private static final String DEFAULT_ERROR_MESSAGE = "There was an error.";


    public UncheckedException(String errorMessage)
    {
        super(errorMessage);
    }


    public UncheckedException(String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments));
    }


    public UncheckedException(Throwable cause, String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments), cause);
    }


    public UncheckedException(Throwable cause)
    {
        super(DEFAULT_ERROR_MESSAGE, cause);
    }
}

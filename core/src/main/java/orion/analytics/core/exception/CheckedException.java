package orion.analytics.core.exception;

public class CheckedException extends Exception
{
    private static final String DEFAULT_ERROR_MESSAGE = "There was an error.";


    public CheckedException(String errorMessage)
    {
        super(errorMessage);
    }


    public CheckedException(String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments));
    }


    public CheckedException(Throwable cause, String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments), cause);
    }


    public CheckedException(Throwable cause)
    {
        super(DEFAULT_ERROR_MESSAGE, cause);
    }
}

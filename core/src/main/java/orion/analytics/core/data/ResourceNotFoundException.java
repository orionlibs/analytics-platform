package orion.analytics.core.data;

import orion.analytics.core.exception.UncheckedException;

public class ResourceNotFoundException extends UncheckedException
{
    private static final String DEFAULT_ERROR_MESSAGE = "There was an error.";


    public ResourceNotFoundException(String errorMessage)
    {
        super(errorMessage);
    }


    public ResourceNotFoundException(String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments));
    }


    public ResourceNotFoundException(Throwable cause, String errorMessage, Object... arguments)
    {
        super(String.format(errorMessage, arguments), cause);
    }


    public ResourceNotFoundException(Throwable cause)
    {
        super(DEFAULT_ERROR_MESSAGE, cause);
    }
}

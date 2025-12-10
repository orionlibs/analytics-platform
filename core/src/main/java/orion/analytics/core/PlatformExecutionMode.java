package orion.analytics.core;

public enum PlatformExecutionMode
{
    SERVER,
    CLIENT;


    public boolean isServer(PlatformExecutionMode other)
    {
        return other.equals(SERVER);
    }


    public boolean isClient(PlatformExecutionMode other)
    {
        return other.equals(CLIENT);
    }
}

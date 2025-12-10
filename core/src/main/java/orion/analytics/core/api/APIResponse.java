package orion.analytics.core.api;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import orion.analytics.core.AError;

@Getter
@Setter
public class APIResponse<DATA> implements Serializable
{
    private Meta meta;
    private AError error;
    private DATA data;


    public APIResponse()
    {
        this.meta = Meta.builder()
                        .traceID(Thread.currentThread().getName())
                        .build();
    }


    public APIResponse(DATA data)
    {
        this();
        this.data = data;
    }


    public <ERROR> APIResponse(AError<ERROR> error, DATA data)
    {
        this(data);
        this.error = error;
    }


    public static APIResponse ofError(AError error)
    {
        APIResponse response = new APIResponse();
        response.setError(error);
        return response;
    }


    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Getter
    public static class Meta implements Serializable
    {
        private String traceID;
    }
}

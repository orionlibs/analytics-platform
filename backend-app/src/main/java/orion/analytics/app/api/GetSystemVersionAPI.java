package orion.analytics.app.api;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import orion.analytics.core.api.APIResponse;
import orion.analytics.core.configuration.Configuration;

@RestController
public class GetSystemVersionAPI
{
    @GetMapping(value = "/system/version")
    public ResponseEntity<APIResponse> getSystemVersion()
    {
        APIResponse<Version> response = new APIResponse<>(Version.builder()
                        .version((String)Configuration.getProp("orion.version"))
                        .build());
        return ResponseEntity.ok(response);
    }


    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    @Getter
    public static class Version implements Serializable
    {
        private String version;
    }
}

package orion.analytics.app.api;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import orion.analytics.core.api.APIResponse;

@RestController
public class GetSystemVersionAPI
{
    @Value("${orion.version}") private String systemVersion;


    @GetMapping(value = "/system/version")
    public ResponseEntity<APIResponse> getSystemVersion()
    {
        APIResponse<Version> response = new APIResponse<>(Version.builder()
                        .version(systemVersion)
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

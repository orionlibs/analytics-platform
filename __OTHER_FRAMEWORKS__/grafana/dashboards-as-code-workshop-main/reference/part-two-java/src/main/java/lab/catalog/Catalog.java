package lab.catalog;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Map;

public class Catalog {
    private final String endpoint;

    public Catalog(String endpoint) {
        this.endpoint = endpoint;
    }

    public static Catalog fromEnv() {
        Map<String, String> env = System.getenv();

        return new Catalog(
            env.getOrDefault("CATALOG_ENDPOINT", "http://localhost:8082/api/services")
        );
    }

    public Service[] services() throws IOException, InterruptedException {
        HttpClient http = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .GET()
                .uri(URI.create(this.endpoint))
                .build();

        HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new RuntimeException("could not fetch service catalog: expected 200, got "+response.statusCode());
        }

        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

        return objectMapper.readValue(response.body(), Service[].class);
    }
}

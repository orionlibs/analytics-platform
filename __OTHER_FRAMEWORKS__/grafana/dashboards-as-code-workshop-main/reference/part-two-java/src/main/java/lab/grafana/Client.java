package lab.grafana;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.grafana.foundation.dashboard.Dashboard;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class Client {
    public String host;
    public String user;
    public String password;

    public Client(String host, String user, String password) {
        this.host = host;
        this.user = user;
        this.password = password;
    }

    public static Client fromEnv() {
        Map<String, String> env = System.getenv();

        return new Client(
                env.getOrDefault("GRAFANA_HOST", "localhost:3000"),
                env.getOrDefault("GRAFANA_USER", "admin"),
                env.getOrDefault("GRAFANA_PASSWORD", "admin")
        );
    }

    public String findOrCreateFolder(String name) throws IOException, InterruptedException {
        HttpClient http = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .GET()
                .uri(URI.create("http://"+this.host+"/api/search?type=dash-folder&query="+ URLEncoder.encode(name, StandardCharsets.UTF_8)))
                .header("Authorization", this.basicAuthenticationHeader())
                .build();

        HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new RuntimeException("could not fetch folders list: expected 200, got "+response.statusCode());
        }

        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        Folder[] folders = objectMapper.readValue(response.body(), Folder[].class);

        // The folder exists.
        if (folders.length == 1) {
            return folders[0].uid;
        }

        // The folder doesn't exist: we create it.
        Map<String, String> payload = new HashMap<>();
        payload.put("title", name);

        request = HttpRequest.newBuilder()
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(payload)))
                .uri(URI.create("http://"+this.host+"/api/folders"))
                .header("Authorization", this.basicAuthenticationHeader())
                .header("Content-Type", "application/json")
                .build();
        response = http.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new RuntimeException("could not create folder: expected 200, got "+response.statusCode());
        }

        Folder folder = objectMapper.readValue(response.body(), Folder.class);

        return folder.uid;
    }

    public void persistDashboard(String folderUid, Dashboard dashboard) throws IOException, InterruptedException {
        HttpClient http = HttpClient.newHttpClient();
        ObjectMapper objectMapper = new ObjectMapper();

        Map<String, Object> payload = new HashMap<>();
        payload.put("dashboard", dashboard);
        payload.put("folderUid", folderUid);
        payload.put("overwrite", true);

        HttpRequest request = HttpRequest.newBuilder()
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(payload)))
                .uri(URI.create("http://"+this.host+"/api/dashboards/db"))
                .header("Authorization", this.basicAuthenticationHeader())
                .header("Content-Type", "application/json")
                .build();

        HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new RuntimeException("could not persist dashboard: expected 200, got "+response.statusCode());
        }
    }

    private String basicAuthenticationHeader() {
        String toEncode = this.user + ":" + this.password;
        return "Basic " + Base64.getEncoder().encodeToString(toEncode.getBytes());
    }

    private static class Folder {
        public String uid;
    }
}

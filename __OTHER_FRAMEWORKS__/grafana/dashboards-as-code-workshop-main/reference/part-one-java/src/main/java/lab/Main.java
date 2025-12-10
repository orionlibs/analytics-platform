package lab;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.grafana.foundation.dashboard.*;
import lab.grafana.Client;
import lab.grafana.Manifest;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class Main {
    private final static String MANIFESTS_DIR = "./resources";
    private final static String DASHBOARD_FOLDER_NAME = "Part one";

    public static void main(String[] args) throws IOException, InterruptedException {
        boolean manifests = List.of(args).contains("--manifests");
        boolean deploy = List.of(args).contains("--deploy");
        boolean help = List.of(args).contains("--help");

        if (help) {
            System.out.println("Usage:");
            System.out.println("\t--deploy\tGenerate and deploy the test dashboard directly to a Grafana instance");
            System.out.println("\t--manifests\tGenerate a dashboard manifest for the test dashboard and write it to disk");
            return;
        }

        Dashboard dashboard = Playground.dashboard().build();

        // Generate a dashboard manifest for the test dashboard and write it to disk.
        if (manifests) {
            generateManifest(dashboard);
            return;
        }

        // Deploy the test dashboard directly to a Grafana instance.
        if (deploy) {
            deployDashboard(dashboard);
            return;
        }

        // By default, print the test dashboard to stdout.
        printDevelopmentDashboard(dashboard);
    }

    private static void deployDashboard(Dashboard dashboard) throws IOException, InterruptedException {
        Client client = Client.fromEnv();
        String folderUid = client.findOrCreateFolder(DASHBOARD_FOLDER_NAME);

        client.persistDashboard(folderUid, dashboard);

        System.out.println("Dashboard deployed");
    }

    private static void generateManifest(Dashboard dashboard) throws IOException, InterruptedException {
        File manifestsDir = new File(MANIFESTS_DIR);

        if (!manifestsDir.exists()) {
            manifestsDir.mkdir();
            manifestsDir.setWritable(true);
        }

        Client client = Client.fromEnv();
        String folderUid = client.findOrCreateFolder(DASHBOARD_FOLDER_NAME);
        com.grafana.foundation.resource.Manifest manifest = Manifest.dashboard(folderUid, dashboard);

        FileWriter manifestWriter = new FileWriter(Path.of(MANIFESTS_DIR, dashboard.uid+".json").toString());
        manifestWriter.write(manifest.toJSON());
        manifestWriter.close();

        System.out.println("Manifest generated in "+MANIFESTS_DIR);
    }

    private static void printDevelopmentDashboard(Dashboard dashboard) throws JsonProcessingException {
        com.grafana.foundation.resource.Manifest manifest = Manifest.dashboard("", dashboard);

        System.out.println(manifest.toJSON());
    }
}

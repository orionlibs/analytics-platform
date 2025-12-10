package lab;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.grafana.foundation.dashboard.*;
import lab.catalog.Catalog;
import lab.catalog.Service;
import lab.grafana.Client;
import lab.grafana.Manifest;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class Main {
    private final static String MANIFESTS_DIR = "./resources";

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

        // Generate a dashboard manifest for the test dashboard and write it to disk.
        if (manifests) {
            generateManifests();
            return;
        }

        // Deploy the test dashboard directly to a Grafana instance.
        if (deploy) {
            deployDashboards();
            return;
        }

        // By default, print the test dashboard to stdout.
        printDevelopmentDashboard();
    }

    private static void deployDashboards() throws IOException, InterruptedException {
        Client client = Client.fromEnv();
        Catalog catalog = Catalog.fromEnv();
        Service[] services = catalog.services();

        for (Service service : services) {
            Dashboard dashboard = Overview.forService(service).build();

            String folderUid = client.findOrCreateFolder(service.name);
            client.persistDashboard(folderUid, dashboard);
        }

        System.out.println("Dashboard deployed");
    }

    private static void generateManifests() throws IOException, InterruptedException {
        File manifestsDir = new File(MANIFESTS_DIR);

        if (!manifestsDir.exists()) {
            manifestsDir.mkdir();
            manifestsDir.setWritable(true);
        }

        Client client = Client.fromEnv();
        Catalog catalog = Catalog.fromEnv();
        Service[] services = catalog.services();

        for (Service service : services) {
            Dashboard dashboard = Overview.forService(service).build();

            String folderUid = client.findOrCreateFolder(service.name);
            com.grafana.foundation.resource.Manifest manifest = Manifest.dashboard(folderUid, dashboard);

            FileWriter manifestWriter = new FileWriter(Path.of(MANIFESTS_DIR, dashboard.uid+".json").toString());
            manifestWriter.write(manifest.toJSON());
            manifestWriter.close();
        }

        System.out.println(services.length + " manifests generated in "+MANIFESTS_DIR);
    }

    private static void printDevelopmentDashboard() throws JsonProcessingException {
        Service service = new Service();
        service.name = "products";
        service.description = "A service related to products";
        service.hasGrpc = true;
        service.hasHttp = true;
        service.repositoryUrl = "http://github.com/org/products-service";

        Dashboard dashboard = Overview.forService(service).build();
        com.grafana.foundation.resource.Manifest manifest = Manifest.dashboard("", dashboard);

        System.out.println(manifest.toJSON());
    }
}

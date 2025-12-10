package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/caarlos0/env/v11"
)

type config struct {
	CatalogEndpoint string `env:"CATALOG_ENDPOINT" envDefault:"http://localhost:8082/api/services"`
	GrafanaHost     string `env:"GRAFANA_HOST" envDefault:"localhost:3000"`
	GrafanaUser     string `env:"GRAFANA_USER" envDefault:"admin"`
	GrafanaPassword string `env:"GRAFANA_PASSWORD" envDefault:"admin"`
}

func main() {
	cfg, err := env.ParseAs[config]()
	if err != nil {
		log.Fatal(err)
	}

	deploy := false
	manifests := false
	manifestsDirectory := "./resources"
	flag.BoolVar(&deploy, "deploy", deploy, "Fetch the list of services from the catalog and deploy a dashboard for each entry")
	flag.BoolVar(&manifests, "manifests", manifests, "Fetch the list of services from the catalog and generate a dashboard manifest for each entry")
	flag.StringVar(&manifestsDirectory, "manifests-directory", manifestsDirectory, "Directory in which the manifests will be generated")
	flag.Parse()

	// Fetch the list services from the catalog and generate a dashboard
	// manifest for each of them.
	if manifests {
		if err := fetchServicesAndGenerateManifests(cfg, manifestsDirectory); err != nil {
			log.Fatal(err)
		}
		return
	}

	// Fetch the list services from the catalog and deploy a dashboard for each
	// of them.
	if deploy {
		if err := fetchServicesAndDeploy(cfg); err != nil {
			log.Fatal(err)
		}
		return
	}

	service := Service{
		Name:          "products",
		HasHTTP:       true,
		HasGRPC:       true,
		Description:   "A service related to products",
		RepositoryURL: "http://github.com/org/products-service",
	}

	printDevelopmentDashboard(service)
}

func fetchServicesAndGenerateManifests(cfg config, outputDir string) error {
	client := grafanaClient(cfg)
	services, err := fetchServices(cfg)
	if err != nil {
		return err
	}

	if err := os.MkdirAll(outputDir, 0777); err != nil {
		return err
	}

	for _, service := range services {
		folderUid, err := findOrCreateFolder(client, service.Name)
		if err != nil {
			return err
		}

		serviceDashboard, err := dashboardForService(service).Build()
		if err != nil {
			return err
		}

		manifest := DashboardManifest(folderUid, serviceDashboard)
		manifestJSON, err := json.MarshalIndent(manifest, "", "  ")
		if err != nil {
			return err
		}

		filename := *serviceDashboard.Uid + ".json"
		if err := os.WriteFile(filepath.Join(outputDir, filename), manifestJSON, 0666); err != nil {
			return err
		}
	}

	return nil
}

func fetchServicesAndDeploy(cfg config) error {
	services, err := fetchServices(cfg)
	if err != nil {
		return err
	}

	client := grafanaClient(cfg)

	for _, service := range services {
		serviceDashboard, err := dashboardForService(service).Build()
		if err != nil {
			return err
		}

		folderUid, err := findOrCreateFolder(client, service.Name)
		if err != nil {
			return err
		}

		err = persistDashboard(client, folderUid, serviceDashboard)
		if err != nil {
			return fmt.Errorf("failed posting dashboard for service '%s': %w", service.Name, err)
		}
	}

	return nil
}

func printDevelopmentDashboard(service Service) {
	serviceDashboard, err := dashboardForService(service).Build()
	if err != nil {
		panic(err)
	}

	manifest := DashboardManifest("", serviceDashboard)
	manifestJSON, err := json.MarshalIndent(manifest, "", "  ")
	if err != nil {
		panic(err)
	}

	fmt.Println(string(manifestJSON))
}

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/caarlos0/env/v11"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
)

const testFolderName = "Part one"

type config struct {
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
	flag.BoolVar(&deploy, "deploy", deploy, "Generate and deploy the test dashboard directly to a Grafana instance")
	flag.BoolVar(&manifests, "manifests", manifests, "Generate a dashboard manifest for the test dashboard and write it to disk")
	flag.StringVar(&manifestsDirectory, "manifests-directory", manifestsDirectory, "Directory in which the manifests will be generated")
	flag.Parse()

	testDashboard, err := testDashboard().Build()
	if err != nil {
		log.Fatal(err)
	}

	// Generate a dashboard manifest for the test dashboard and write it to disk.
	if manifests {
		if err := generateManifest(cfg, manifestsDirectory, testDashboard); err != nil {
			log.Fatal(err)
		}
		return
	}

	// Deploy the test dashboard directly to a Grafana instance.
	if deploy {
		if err := deployDashboard(cfg, testDashboard); err != nil {
			log.Fatal(err)
		}
		return
	}

	// By default: print the test dashboard to stdout.
	printDashboard(testDashboard)
}

func generateManifest(cfg config, outputDir string, dashboard dashboard.Dashboard) error {
	client := grafanaClient(cfg)

	if err := os.MkdirAll(outputDir, 0777); err != nil {
		return err
	}

	folderUid, err := findOrCreateFolder(client, testFolderName)
	if err != nil {
		return err
	}

	manifest := DashboardManifest(folderUid, dashboard)
	manifestJSON, err := json.MarshalIndent(manifest, "", "  ")
	if err != nil {
		return err
	}

	filename := *dashboard.Uid + ".json"
	if err := os.WriteFile(filepath.Join(outputDir, filename), manifestJSON, 0666); err != nil {
		return err
	}

	return nil
}

func deployDashboard(cfg config, dashboard dashboard.Dashboard) error {
	client := grafanaClient(cfg)

	folderUid, err := findOrCreateFolder(client, testFolderName)
	if err != nil {
		return err
	}

	err = persistDashboard(client, folderUid, dashboard)
	if err != nil {
		return fmt.Errorf("failed posting dashboard: %w", err)
	}

	return nil
}

func printDashboard(dashboard dashboard.Dashboard) {
	manifest := DashboardManifest("", dashboard)
	manifestJSON, err := json.MarshalIndent(manifest, "", "  ")
	if err != nil {
		panic(err)
	}

	fmt.Println(string(manifestJSON))
}

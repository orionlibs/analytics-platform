package main

import (
	"net/url"
	"strings"

	"github.com/go-openapi/strfmt"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
	"github.com/grafana/grafana-foundation-sdk/go/resource"
	gapi "github.com/grafana/grafana-openapi-client-go/client"
	"github.com/grafana/grafana-openapi-client-go/client/folders"
	"github.com/grafana/grafana-openapi-client-go/models"
)

func DashboardManifest(folderUid string, dash dashboard.Dashboard) resource.Manifest {
	return resource.Manifest{
		ApiVersion: "dashboard.grafana.app/v1beta1",
		Kind:       "Dashboard",
		Metadata: resource.Metadata{
			Annotations: map[string]string{
				"grafana.app/folder": folderUid,
			},
			Name: *dash.Uid,
		},
		Spec: dash,
	}
}

func grafanaClient(cfg config) *gapi.GrafanaHTTPAPI {
	return gapi.NewHTTPClientWithConfig(strfmt.Default, &gapi.TransportConfig{
		// Host is the domain name or IP address of the host that serves the API.
		Host: cfg.GrafanaHost,
		// BasePath is the URL prefix for all API paths, relative to the host root.
		BasePath: "/api",
		// Schemes are the transfer protocols used by the API (http or https).
		Schemes: []string{"http"},
		// BasicAuth is contains basic auth credentials.
		BasicAuth: url.UserPassword(cfg.GrafanaUser, cfg.GrafanaPassword),
	})
}

func findOrCreateFolder(gapi *gapi.GrafanaHTTPAPI, folderName string) (string, error) {
	// FIXME: this doesn't handle pagination.
	// It will misbehave if the target Grafana instance has >1000 folders.
	getParams := folders.NewGetFoldersParams()
	response, err := gapi.Folders.GetFolders(getParams)
	if err != nil {
		return "", err
	}

	for _, folder := range response.Payload {
		if strings.EqualFold(folder.Title, folderName) {
			return folder.UID, nil
		}
	}

	// The folder doesn't exist: create it.
	createResponse, err := gapi.Folders.CreateFolder(&models.CreateFolderCommand{
		Title: folderName,
	})
	if err != nil {
		return "", err
	}

	return createResponse.Payload.UID, nil
}

func persistDashboard(gapi *gapi.GrafanaHTTPAPI, folderUID string, dash dashboard.Dashboard) error {
	_, err := gapi.Dashboards.PostDashboard(&models.SaveDashboardCommand{
		FolderUID: folderUID,
		Dashboard: dash,
		Overwrite: true,
	})

	return err
}

package main

import (
	"encoding/json"
	"net/http"
)

type Service struct {
	Name          string `json:"name"`
	Description   string `json:"description"`
	HasHTTP       bool   `json:"has_http"`
	HasGRPC       bool   `json:"has_grpc"`
	RepositoryURL string `json:"github"`
}

func fetchServices(cfg config) ([]Service, error) {
	response, err := http.Get(cfg.CatalogEndpoint)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()

	services := make([]Service, 0)
	if err := json.NewDecoder(response.Body).Decode(&services); err != nil {
		return nil, err
	}

	return services, nil
}

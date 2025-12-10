package plugin

import (
	"encoding/json"
	"errors"
	"github.com/grafana/grafana-plugin-sdk-go/backend"
)

type jsonData struct {
	Owner  string `json:"owner"`
	Repo   string `json:"repo"`
	Source string `json:"source"`
}

type Settings struct {
	jsonData
	AuthToken string
}

func UnmarshalRawInstanceSettings(rawInstanceSettings backend.DataSourceInstanceSettings) (Settings, error) {

	settings := Settings{}

	err := json.Unmarshal(rawInstanceSettings.JSONData, &settings)

	if err != nil {
		return settings, err
	}

	settings.AuthToken = rawInstanceSettings.DecryptedSecureJSONData["authToken"]

	if settings.AuthToken == "" {
		return settings, errors.New("Auth token was not set")
	}

	return settings, nil
}

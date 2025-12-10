//go:build mage
// +build mage

package main

import (
	// mage:import
	build "github.com/grafana/grafana-plugin-sdk-go/build"
)

var err = build.SetBeforeBuildCallback(func(cfg build.Config) (build.Config, error) {
	cfg.PluginJSONPath = "src/datasource"
	cfg.OutputBinaryPath = "dist/datasource"
	return cfg, nil
})

// Default configures the default target.
var Default = build.BuildAll

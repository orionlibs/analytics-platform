// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

package spansanitizeprocessor // import "github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor"

import "go.opentelemetry.io/collector/confmap/xconfmap"

// Config defines the configuration options for the Grafana Cloud connector.
type Config struct {
	// DebugMode is a boolean that indicates if the debug mode is enabled.
	// If enabled, the processor will preserve the original span name in the "old.span.name" attribute	.
	DebugMode bool `mapstructure:"debug_mode"`
	// prevent unkeyed literal initialization
	_ struct{}
}

var _ xconfmap.Validator = (*Config)(nil)

// Validate checks if the configuration is valid
func (c Config) Validate() error {
	return nil
}

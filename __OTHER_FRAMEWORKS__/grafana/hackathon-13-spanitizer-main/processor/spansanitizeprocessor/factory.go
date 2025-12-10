// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

package spansanitizeprocessor // import "github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor"

import (
	"context"

	"go.opentelemetry.io/collector/component"
	"go.opentelemetry.io/collector/consumer"
	"go.opentelemetry.io/collector/processor"
	"go.opentelemetry.io/collector/processor/processorhelper"

	clusterurl "github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor/internal/clusterurl"
	"github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor/internal/metadata"
)

var processorCapabilities = consumer.Capabilities{MutatesData: true}

// NewFactory returns a new factory for the SpanSanitize processor.
func NewFactory() processor.Factory {
	return processor.NewFactory(
		metadata.Type,
		createDefaultConfig,
		processor.WithTraces(createTracesProcessor, component.StabilityLevelDevelopment))
}

func createDefaultConfig() component.Config {
	return &Config{}
}

func createTracesProcessor(
	ctx context.Context,
	set processor.Settings,
	baseCfg component.Config,
	next consumer.Traces,
) (processor.Traces, error) {
	cfg := baseCfg.(*Config)
	classifier, err := clusterurl.NewClusterUrlClassifier(clusterurl.DefaultConfig())
	if err != nil {
		return nil, err
	}

	cusp, err := newSpanSanitizeProcessor(set, cfg, classifier)
	if err != nil {
		return nil, err
	}

	return processorhelper.NewTraces(
		ctx,
		set,
		cfg,
		next,
		cusp.processTraces,
		processorhelper.WithCapabilities(processorCapabilities),
	)
}

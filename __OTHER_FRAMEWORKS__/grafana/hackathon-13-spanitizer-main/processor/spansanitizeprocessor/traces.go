// Copyright The OpenTelemetry Authors
// SPDX-License-Identifier: Apache-2.0

package spansanitizeprocessor // import "github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor"

import (
	"context"

	clusterurl "github.com/open-telemetry/opentelemetry-collector-contrib/processor/spansanitizeprocessor/internal/clusterurl"
	"go.opentelemetry.io/collector/pdata/ptrace"
	"go.opentelemetry.io/collector/processor"
	"go.uber.org/zap"
)

type spanSanitizeProcessor struct {
	config     Config
	logger     *zap.Logger
	classifier *clusterurl.ClusterUrlClassifier
}

func newSpanSanitizeProcessor(set processor.Settings, cfg *Config, classifier *clusterurl.ClusterUrlClassifier) (*spanSanitizeProcessor, error) {
	cusp := &spanSanitizeProcessor{
		config:     *cfg,
		logger:     set.Logger,
		classifier: classifier,
	}

	cusp.logger.Info("Creating SpanSanitizeProcessor")

	return cusp, nil
}

// ConsumeTraces implements processor.Traces.
func (cusp *spanSanitizeProcessor) processTraces(_ context.Context, td ptrace.Traces) (ptrace.Traces, error) {
	for i := 0; i < td.ResourceSpans().Len(); i++ {
		resourceSpan := td.ResourceSpans().At(i)

		for j := 0; j < resourceSpan.ScopeSpans().Len(); j++ {
			scopeSpan := resourceSpan.ScopeSpans().At(j)

			for k := 0; k < scopeSpan.Spans().Len(); k++ {
				span := scopeSpan.Spans().At(k)
				if span.Kind() == ptrace.SpanKindServer || span.Kind() == ptrace.SpanKindClient {
					// Check if the span has the HTTP method set, which indicates it's an HTTP span.
					var ok bool
					_, ok = span.Attributes().Get("http.request.method")
					// Fallback to old http.method
					if !ok {
						_, ok = span.Attributes().Get("http.method")
					}
					if ok {
						spanName := span.Name()
						span.SetName(cusp.classifier.ClusterURL(spanName))
						if cusp.config.DebugMode {
							span.Attributes().PutStr("old.span.name", spanName)
						}
					}
				}
			}
		}
	}
	return td, nil
}

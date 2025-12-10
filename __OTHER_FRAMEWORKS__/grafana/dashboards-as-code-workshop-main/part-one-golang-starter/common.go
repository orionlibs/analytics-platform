package main

import (
	"github.com/grafana/grafana-foundation-sdk/go/cog"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
	"github.com/grafana/grafana-foundation-sdk/go/logs"
	"github.com/grafana/grafana-foundation-sdk/go/loki"
	"github.com/grafana/grafana-foundation-sdk/go/prometheus"
	"github.com/grafana/grafana-foundation-sdk/go/stat"
	"github.com/grafana/grafana-foundation-sdk/go/text"
	"github.com/grafana/grafana-foundation-sdk/go/timeseries"
)

// This file contains a series of utility functions to simplify the creation
// of panels while providing a consistent "look and feel".

// statPanel creates a pre-configured stat panel.
func statPanel() *stat.PanelBuilder {
	// no specific options required for this lab.
	return stat.NewPanelBuilder()
}

// textPanel creates a text panel pre-configured for markdown content.
func textPanel(content string) *text.PanelBuilder {
	return text.NewPanelBuilder()
	// TODO: configure default options for text panels
	//
	//  * `content` set to content
	//  * `mode` set to `markdown`
	//
	// See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/go/Reference/text/builder-PanelBuilder/
}

// timeseriesPanel creates a pre-configured timeseries panel.
func timeseriesPanel() *timeseries.PanelBuilder {
	return timeseries.NewPanelBuilder()
	// TODO: configure default options for timeseries panels
	//
	//  * `fillOpacity` set to `20`
	//  * `gradientMode` set to  `opacity`
	//  * `legend` options:
	//    * `displayMode` set to `list`
	//    * `placement` set to `bottom`
	//    * `showLegend` set to `true`
	//
	// See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/go/Reference/timeseries/builder-PanelBuilder/
}

// logPanel creates a pre-configured logs panel.
func logPanel() *logs.PanelBuilder {
	return logs.NewPanelBuilder()
	// TODO: configure default options for logs panels
	//
	//  * `showTime` set to `true`
	//  * `sortOrder` set to `Descending`
	//  * `enableLogDetails` set to `true`
	//
	// See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/go/Reference/logs/builder-PanelBuilder/
}

// prometheusQuery creates a Prometheus query pre-configured for range vectors.
func prometheusQuery(expression string) *prometheus.DataqueryBuilder {
	return prometheus.NewDataqueryBuilder().
		Expr(expression).
		Range().
		Format(prometheus.PromQueryFormatTimeSeries).
		LegendFormat("__auto")
}

// instantPrometheusQuery creates a Prometheus query pre-configured for instant
// vectors and table data formatting.
func instantPrometheusQuery(expression string) *prometheus.DataqueryBuilder {
	return prometheus.NewDataqueryBuilder().
		Expr(expression).
		Instant().
		Format(prometheus.PromQueryFormatTable).
		LegendFormat("__auto")
}

// lokiQuery creates a Loki query pre-configured for range vectors.
func lokiQuery(expression string) *loki.DataqueryBuilder {
	return loki.NewDataqueryBuilder().
		Expr(expression).
		QueryType("range").
		LegendFormat("__auto")
}

// prometheusDatasourceRef returns a reference to the Prometheus datasource
// used by the workshop stack.
func prometheusDatasourceRef() dashboard.DataSourceRef {
	return dashboard.DataSourceRef{
		Type: cog.ToPtr("prometheus"),
		Uid:  cog.ToPtr("prometheus"),
	}
}

// lokiDatasourceRef returns a reference to the Loki datasource used by the
// workshop stack.
func lokiDatasourceRef() dashboard.DataSourceRef {
	return dashboard.DataSourceRef{
		Type: cog.ToPtr("loki"),
		Uid:  cog.ToPtr("loki"),
	}
}

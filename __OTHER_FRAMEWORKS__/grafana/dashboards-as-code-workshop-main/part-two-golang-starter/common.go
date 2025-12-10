package main

import (
	"github.com/grafana/grafana-foundation-sdk/go/cog"
	"github.com/grafana/grafana-foundation-sdk/go/common"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
	"github.com/grafana/grafana-foundation-sdk/go/heatmap"
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
	return stat.NewPanelBuilder()
}

// textPanel creates a text panel pre-configured for markdown content.
func textPanel(content string) *text.PanelBuilder {
	return text.NewPanelBuilder().
		Mode(text.TextModeMarkdown).
		Content(content)
}

// timeseriesPanel creates a pre-configured timeseries panel.
func timeseriesPanel() *timeseries.PanelBuilder {
	return timeseries.NewPanelBuilder().
		FillOpacity(20).
		GradientMode(common.GraphGradientModeOpacity).
		Legend(common.NewVizLegendOptionsBuilder().
			DisplayMode(common.LegendDisplayModeList).
			Placement(common.LegendPlacementBottom).
			ShowLegend(true),
		)
}

// heatmapPanel creates a pre-configured heatmap panel.
func heatmapPanel() *heatmap.PanelBuilder {
	return heatmap.NewPanelBuilder().
		Color(heatmap.NewHeatmapColorOptionsBuilder().
			Mode(heatmap.HeatmapColorModeScheme).
			Scheme("RdYlBu").
			Scale(heatmap.HeatmapColorScaleExponential).
			Steps(64),
		).
		FilterValues(heatmap.NewFilterValueRangeBuilder().Le(1e-09)).
		YAxis(heatmap.NewYAxisConfigBuilder().Unit("s")).
		Mode(common.TooltipDisplayModeSingle).
		ScaleDistribution(common.NewScaleDistributionConfigBuilder().Type("linear"))
}

// logPanel creates a pre-configured logs panel.
func logPanel() *logs.PanelBuilder {
	return logs.NewPanelBuilder().
		Datasource(lokiDatasourceRef()).
		ShowTime(true).
		SortOrder(common.LogsSortOrderDescending).
		EnableLogDetails(true)
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

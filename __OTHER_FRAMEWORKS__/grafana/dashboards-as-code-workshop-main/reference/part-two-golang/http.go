package main

import (
	"fmt"

	"github.com/grafana/grafana-foundation-sdk/go/heatmap"
	"github.com/grafana/grafana-foundation-sdk/go/logs"
	"github.com/grafana/grafana-foundation-sdk/go/prometheus"
	"github.com/grafana/grafana-foundation-sdk/go/timeseries"
	"github.com/grafana/grafana-foundation-sdk/go/units"
)

func httpRequestsTimeseries(service Service) *timeseries.PanelBuilder {
	return timeseriesPanel().
		Title("HTTP Requests").
		Unit(units.RequestsPerSecond).
		WithTarget(prometheusQuery(fmt.Sprintf("rate(http_requests_total{service=\"%s\"}[$__rate_interval])", service.Name)).
			LegendFormat("{{code}} - {{ method }} {{ path }}"),
		).
		Datasource(prometheusDatasourceRef())
}

func httpLatenciesHeatmap(service Service) *heatmap.PanelBuilder {
	return heatmapPanel().
		Title("HTTP Requests latencies").
		WithTarget(prometheusQuery(fmt.Sprintf("sum(increase(http_requests_duration_seconds_bucket{service=\"%s\"}[$__rate_interval])) by (le)", service.Name)).
			Format(prometheus.PromQueryFormatHeatmap),
		).
		Datasource(prometheusDatasourceRef())
}

func httpLogsPanel(service Service) *logs.PanelBuilder {
	return logPanel().
		Title("HTTP Logs").
		WithTarget(lokiQuery(fmt.Sprintf("{service=\"%s\", source=\"http\", level=~\"$logs_level\"} |~ \"$logs_filter\"", service.Name)))
}

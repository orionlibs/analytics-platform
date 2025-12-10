package main

import (
	"fmt"

	"github.com/grafana/grafana-foundation-sdk/go/heatmap"
	"github.com/grafana/grafana-foundation-sdk/go/logs"
	"github.com/grafana/grafana-foundation-sdk/go/prometheus"
	"github.com/grafana/grafana-foundation-sdk/go/timeseries"
	"github.com/grafana/grafana-foundation-sdk/go/units"
)

func grpcRequestsTimeseries(service Service) *timeseries.PanelBuilder {
	return timeseriesPanel().
		Title("gRPC Requests").
		Unit(units.RequestsPerSecond).
		WithTarget(prometheusQuery(fmt.Sprintf("rate(grpc_server_handled_total{service=\"%s\"}[$__rate_interval])", service.Name)).
			LegendFormat("{{ grpc_method }} – {{ grpc_code }}"),
		).
		Datasource(prometheusDatasourceRef())
}

func grpcLatenciesHeatmap(service Service) *heatmap.PanelBuilder {
	return heatmapPanel().
		Title("gRPC Requests latencies").
		WithTarget(prometheusQuery(fmt.Sprintf("sum(increase(grpc_server_handling_seconds_bucket{service=\"%s\"}[$__rate_interval])) by (le)", service.Name)).
			Format(prometheus.PromQueryFormatHeatmap),
		).
		Datasource(prometheusDatasourceRef())
}

func grpcLogsPanel(service Service) *logs.PanelBuilder {
	return logPanel().
		Title("gRPC Logs").
		WithTarget(lokiQuery(fmt.Sprintf("{service=\"%s\", source=\"grpc\", level=~\"$logs_level\"} |~ \"$logs_filter\"", service.Name)))
}

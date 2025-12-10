package main

import (
	"github.com/grafana/grafana-foundation-sdk/go/common"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
	"github.com/grafana/grafana-foundation-sdk/go/logs"
	"github.com/grafana/grafana-foundation-sdk/go/stat"
	"github.com/grafana/grafana-foundation-sdk/go/text"
	"github.com/grafana/grafana-foundation-sdk/go/timeseries"
)

func testDashboard() *dashboard.DashboardBuilder {
	builder := dashboard.NewDashboardBuilder("Test dashboard").
		Uid("test-dashboard").
		Tags([]string{"test", "generated"}).
		Time("now-30m", "now").
		Tooltip(dashboard.DashboardCursorSyncCrosshair).
		Refresh("10s")

	builder.
		WithPanel(prometheusVersionStat()).
		WithPanel(descriptionText()).
		WithPanel(unfilteredLogs()).
		WithPanel(prometheusGoroutinesTimeseries())

	return builder
}

func prometheusVersionStat() *stat.PanelBuilder {
	return statPanel().
		Title("Prometheus version").
		WithTarget(
			instantPrometheusQuery("prometheus_build_info{}"),
		).
		Transparent(true).
		Datasource(prometheusDatasourceRef()).
		ReduceOptions(common.NewReduceDataOptionsBuilder().
			Calcs([]string{"last"}).
			Fields("/^version$/"),
		)
}

func descriptionText() *text.PanelBuilder {
	return textPanel("Text panels are supported too! Even with *markdown* text :)").
		Transparent(true)
}

func unfilteredLogs() *logs.PanelBuilder {
	return logPanel().
		Title("Logs").
		Datasource(lokiDatasourceRef()).
		WithTarget(lokiQuery("{job=\"app_logs\"}"))
}

func prometheusGoroutinesTimeseries() *timeseries.PanelBuilder {
	return timeseriesPanel().
		Title("Prometheus goroutines").
		Datasource(prometheusDatasourceRef()).
		WithTarget(prometheusQuery("go_goroutines{job=\"prometheus\"}"))
}

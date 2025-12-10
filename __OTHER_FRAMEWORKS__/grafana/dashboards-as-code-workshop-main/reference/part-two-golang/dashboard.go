package main

import (
	"fmt"

	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
)

func dashboardForService(service Service) *dashboard.DashboardBuilder {
	builder := dashboard.NewDashboardBuilder(fmt.Sprintf("%s service overview", service.Name)).
		Uid(fmt.Sprintf("%s-overview", service.Name)).
		Tags([]string{service.Name, "generated"}).
		Readonly().
		Time("now-30m", "now").
		Tooltip(dashboard.DashboardCursorSyncCrosshair).
		Refresh("10s").
		Link(dashboard.NewDashboardLinkBuilder("GitHub Repository").
			Type(dashboard.DashboardLinkTypeLink).
			Url(service.RepositoryURL).
			TargetBlank(true),
		).
		WithVariable(dashboard.NewTextBoxVariableBuilder("logs_filter").
			Label("Logs filter"),
		).
		WithVariable(logLevelsVariable(service))

	// Overview
	builder.
		WithPanel(versionStat(service).Height(4).Span(4)).
		WithPanel(descriptionText(service).Height(4).Span(4)).
		WithPanel(logsVolumeTimeseries(service).Height(4).Span(16))

	// gRPC row, if relevant
	if service.HasGRPC {
		builder.WithRow(dashboard.NewRowBuilder("gRPC")).
			WithPanel(grpcRequestsTimeseries(service).Height(8)).
			WithPanel(grpcLatenciesHeatmap(service).Height(8)).
			WithPanel(grpcLogsPanel(service).Height(8).Span(24))
	}

	// HTTP row, if relevant
	if service.HasHTTP {
		builder.
			WithRow(dashboard.NewRowBuilder("HTTP")).
			WithPanel(httpRequestsTimeseries(service).Height(8)).
			WithPanel(httpLatenciesHeatmap(service).Height(8)).
			WithPanel(httpLogsPanel(service).Height(8).Span(24))

	}

	return builder
}

func logLevelsVariable(service Service) *dashboard.QueryVariableBuilder {
	return dashboard.NewQueryVariableBuilder("logs_level").
		Label("Logs level").
		Datasource(lokiDatasourceRef()).
		Query(dashboard.StringOrMap{
			Map: map[string]any{
				"label":  "level",
				"stream": fmt.Sprintf(`{service="%s"}`, service.Name),
				"type":   1,
			},
		}).
		Refresh(dashboard.VariableRefreshOnTimeRangeChanged).
		IncludeAll(true).
		AllValue(".*")
}

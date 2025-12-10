from grafana_foundation_sdk.builders import dashboard
from grafana_foundation_sdk.models.dashboard import (
    DashboardCursorSync,
    VariableRefresh,
)

from .catalog import Service
from .common import loki_datasource_ref
from . import grpc, http, overview


def dashboard_for_service(service: Service) -> dashboard.Dashboard:
    builder = (
        dashboard.Dashboard(f"{service.name} service overview")
        .uid(f"{service.name}-overview")
        .tags([service.name, "generated"])
        .readonly()
        .time("now-30m", "now")
        .tooltip(DashboardCursorSync.CROSSHAIR)
        .refresh("10s")
        .link(
            dashboard.DashboardLink("GitHub Repository")
            .url(service.repository_url)
            .target_blank(True)
        )
        .with_variable(dashboard.TextBoxVariable("logs_filter").label("Logs filter"))
        .with_variable(log_levels_variable(service))
    )

    # Overview
    builder.with_panel(overview.version_stat(service).height(4).span(4))
    builder.with_panel(overview.description_text(service).height(4).span(4))
    builder.with_panel(overview.logs_volume_timeseries(service).height(4).span(16))

    # gRPC row, if relevant
    if service.has_grpc:
        builder.with_row(dashboard.Row("gRPC"))
        builder.with_panel(grpc.requests_timeseries(service).height(8))
        builder.with_panel(grpc.latencies_heatmap(service).height(8))
        builder.with_panel(grpc.service_logs(service).height(8).span(24))

    # HTTP row, if relevant
    if service.has_http:
        builder.with_row(dashboard.Row("HTTP"))
        builder.with_panel(http.requests_timeseries(service).height(8))
        builder.with_panel(http.latencies_heatmap(service).height(8))
        builder.with_panel(http.service_logs(service).height(8).span(24))

    return builder


def log_levels_variable(service: Service) -> dashboard.QueryVariable:
    return (
        dashboard.QueryVariable("logs_level")
        .label("Logs level")
        .datasource(loki_datasource_ref())
        .query(
            {
                "label": "level",
                "stream": '{service="%s"}' % service.name,
                "type": 1,
            }
        )
        .refresh(VariableRefresh.ON_TIME_RANGE_CHANGED)
        .include_all(True)
        .all_value(".*")
    )


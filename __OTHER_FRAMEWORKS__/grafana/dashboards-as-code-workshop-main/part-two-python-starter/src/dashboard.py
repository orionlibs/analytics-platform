from grafana_foundation_sdk.builders import dashboard
from grafana_foundation_sdk.models.dashboard import (
    DashboardCursorSync,
    VariableRefresh,
)

from .catalog import Service
from .common import loki_datasource_ref


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

    # TODO:
    # * "Version" panel
    #   - type: `stat`
    #   - query: `app_infos{service="[service_name]"}`
    #     - instant: true
    #   - datasource: Prometheus datasource ref (see common.prometheus_datasource_ref())
    #   - transparent: true
    #   - reduce options:
    #     - values: false
    #     - calcs: ["last"]
    #     - fields: "/^version$/"
    #   - height: 4
    #   - span: 4
    # * "service description" panel
    #   - type: `text`
    #   - transparent: true
    #   - height: 4
    #   - span: 4
    # * "Logs volume" panel. Height: 4, Span: 16
    #   - type: `timeseries`
    #   - query: `sum by (level) (count_over_time({service="[service_name]", level=~"$logs_level"} |~ "$logs_filter" [$__auto]))`
    #     - legend format: `{{level}}`
    #   - stacking mode: normal
    #   - `legend` options:
    #     - displayMode: `list`
    #     - placement: `bottom`
    #     - showLegend: `true`
    #   - draw style: bars
    #   - override by name:
    #     - name: "INFO"
    #     - value: `color = {"mode": "fixed", "fixedColor": "green"}`
    #   - override by name:
    #     - name: "ERROR"
    #     - value: `color = {"mode": "fixed", "fixedColor": "red"}`
    #   - height: 4
    #   - span: 16

    # gRPC row, if relevant
    # TODO: define a "gRPC" row with the following panels:
    # * "gRPC Requests" panel
    #   - type: `timeseries`
    #   - query: `rate(grpc_server_handled_total{service="[service_name]"}[$__rate_interval])`
    #   - datasource: Prometheus datasource ref (see common.prometheus_datasource_ref())
    #   - query legend format: `{{ grpc_method }} – {{ grpc_code }}`
    #   - unit: requests per second (reqps)
    #   - height: 8
    #   - span: 12
    # * "gRPC Requests latencies" panel
    #   - type: `heatmap`
    #   - query: `sum(increase(grpc_server_handling_seconds_bucket{service="[service_name]"}[$__rate_interval])) by (le)`
    #   - query format: `heatmap`
    #   - datasource: Prometheus datasource ref (see common.prometheus_datasource_ref())
    #   - height: 8
    #   - span: 12
    # * "GRPC Logs" panel
    #   - type: `logs`
    #   - query: `{service="[service_name]", source="grpc", level=~"$logs_level"} |~ "$logs_filter"`
    #   - height: 8
    #   - span: 24

    # HTTP row, if relevant
    # TODO: define an "HTTP" row with the following panels:
    # * "HTTP Requests" panel
    #   - type: `timeseries`
    #   - query: `rate(http_requests_total{service="[service_name]"}[$__rate_interval])`
    #   - datasource: Prometheus datasource ref (see common.prometheus_datasource_ref())
    #   - query legend format: `{{code}} - {{ method }} {{ path }}`
    #   - unit: requests per second (reqps)
    #   - height: 8
    #   - span: 12
    # * "HTTP Requests latencies" panel
    #   - type: `heatmap`
    #   - query: `sum(increase(http_requests_duration_seconds_bucket{service="[service_name]"}[$__rate_interval])) by (le)`
    #   - query format: `heatmap`
    #   - datasource: Prometheus datasource ref (see common.prometheus_datasource_ref())
    #   - height: 8
    #   - span: 12
    # * "HTTP Logs" panel
    #   - type: `logs`
    #   - query: `{service="[service_name]", source="http", level=~"$logs_level"} |~ "$logs_filter"`
    #   - height: 8
    #   - span: 24

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


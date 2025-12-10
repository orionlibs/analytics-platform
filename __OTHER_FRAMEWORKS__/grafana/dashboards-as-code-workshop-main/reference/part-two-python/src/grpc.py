from grafana_foundation_sdk.builders import heatmap, logs, timeseries
from grafana_foundation_sdk.models.prometheus import PromQueryFormat
from grafana_foundation_sdk.models.units import RequestsPerSecond

from .catalog import Service
from .common import (
    prometheus_datasource_ref,
    loki_query,
    prometheus_query,
    timeseries_panel,
    heatmap_panel,
    log_panel,
)


def requests_timeseries(service: Service) -> timeseries.Panel:
    return (
        timeseries_panel()
        .title("gRPC Requests")
        .unit(RequestsPerSecond)
        .with_target(
            prometheus_query(
                'rate(grpc_server_handled_total{service="%s"}[$__rate_interval])'
                % service.name
            ).legend_format("{{ grpc_method }} – {{ grpc_code }}")
        )
        .datasource(prometheus_datasource_ref())
    )


def latencies_heatmap(service: Service) -> heatmap.Panel:
    return (
        heatmap_panel()
        .title("gRPC Requests latencies")
        .with_target(
            prometheus_query(
                'sum(increase(grpc_server_handling_seconds_bucket{service="%s"}[$__rate_interval])) by (le)'
                % service.name
            ).format(PromQueryFormat.HEATMAP)
        )
        .datasource(prometheus_datasource_ref())
    )


def service_logs(service: Service) -> logs.Panel:
    return (
        log_panel()
        .title("gRPC logs")
        .with_target(
            loki_query(
                '{service="%s", source="grpc", level=~"$logs_level"} |~ "$logs_filter"'
                % service.name
            )
        )
    )

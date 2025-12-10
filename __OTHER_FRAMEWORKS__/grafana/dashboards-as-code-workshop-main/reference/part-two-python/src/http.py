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
        .title("HTTP Requests")
        .unit(RequestsPerSecond)
        .with_target(
            prometheus_query(
                'rate(http_requests_total{service="%s"}[$__rate_interval])'
                % service.name
            ).legend_format("{{code}} - {{ method }} {{ path }}")
        )
        .datasource(prometheus_datasource_ref())
    )


def latencies_heatmap(service: Service) -> heatmap.Panel:
    return (
        heatmap_panel()
        .title("HTTP Requests latencies")
        .unit("reqps")
        .with_target(
            prometheus_query(
                'sum(increase(http_requests_duration_seconds_bucket{service="%s"}[$__rate_interval])) by (le)'
                % service.name
            ).format(PromQueryFormat.HEATMAP)
        )
        .datasource(prometheus_datasource_ref())
    )


def service_logs(service: Service) -> logs.Panel:
    return (
        log_panel()
        .title("HTTP logs")
        .with_target(
            loki_query(
                '{service="%s", source="http", level=~"$logs_level"} |~ "$logs_filter"'
                % service.name
            )
        )
    )

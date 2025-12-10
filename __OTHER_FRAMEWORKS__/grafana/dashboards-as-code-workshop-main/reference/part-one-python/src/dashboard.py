from grafana_foundation_sdk.builders import (
    common,
    dashboard,
    logs,
    stat,
    text,
    timeseries,
)
from grafana_foundation_sdk.models.dashboard import DashboardCursorSync

from .common import (
    prometheus_datasource_ref,
    loki_query,
    loki_datasource_ref,
    instant_prometheus_query,
    prometheus_query,
    timeseries_panel,
    log_panel,
    stat_panel,
    text_panel,
)


def example_dashboard() -> dashboard.Dashboard:
    builder = (
        dashboard.Dashboard("Test dashboard")
        .uid("test-dashboard")
        .tags(["test", "generated"])
        .readonly()
        .time("now-30m", "now")
        .tooltip(DashboardCursorSync.CROSSHAIR)
        .refresh("10s")
    )

    builder.with_panel(prometheus_version_stat())
    builder.with_panel(description_text())
    builder.with_panel(unfiltered_logs())
    builder.with_panel(prometheus_goroutines_timeseries())

    return builder


def prometheus_version_stat() -> stat.Panel:
    return (
        stat_panel()
        .title("Prometheus version")
        .with_target(instant_prometheus_query("prometheus_build_info{}"))
        .transparent(True)
        .datasource(prometheus_datasource_ref())
        .reduce_options(
            common.ReduceDataOptions().calcs(["last"]).fields("/^version$/")
        )
    )


def description_text() -> text.Panel:
    return text_panel(
        "Text panels are supported too! Even with *markdown* text :)"
    ).transparent(True)


def unfiltered_logs() -> logs.Panel:
    return (
        log_panel()
        .title("Logs")
        .with_target(loki_query('{job="app_logs"}'))
        .datasource(loki_datasource_ref())
    )


def prometheus_goroutines_timeseries() -> timeseries.Panel:
    return (
        timeseries_panel()
        .title("Prometheus goroutines")
        .with_target(prometheus_query('go_goroutines{job="prometheus"}'))
        .datasource(prometheus_datasource_ref())
    )

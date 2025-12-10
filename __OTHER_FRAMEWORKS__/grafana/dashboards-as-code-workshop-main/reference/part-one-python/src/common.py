from grafana_foundation_sdk.builders import (
    common,
    logs,
    loki,
    prometheus,
    stat,
    text,
    timeseries,
)
from grafana_foundation_sdk.models.common import (
    LogsSortOrder,
    GraphGradientMode,
    LegendDisplayMode,
    LegendPlacement,
)
from grafana_foundation_sdk.models.dashboard import DataSourceRef
from grafana_foundation_sdk.models.prometheus import PromQueryFormat
from grafana_foundation_sdk.models.text import TextMode

# This file contains a series of utility functions to simplify the creation
# of panels while providing a consistent "look and feel".


def stat_panel() -> stat.Panel:
    """
    Creates a pre-configured stat panel.
    """
    return stat.Panel()


def text_panel(content: str) -> text.Panel:
    """
    Creates a pre-configured text panel.
    """
    return text.Panel().mode(TextMode.MARKDOWN).content(content)


def timeseries_panel() -> timeseries.Panel:
    """
    Creates a pre-configured timeseries panel.
    """
    return (
        timeseries.Panel()
        .fill_opacity(20)
        .gradient_mode(GraphGradientMode.OPACITY)
        .legend(
            common.VizLegendOptions()
            .display_mode(LegendDisplayMode.LIST)
            .placement(LegendPlacement.BOTTOM)
            .show_legend(True)
        )
    )


def log_panel() -> logs.Panel:
    """
    Creates a pre-configured logs panel.
    """
    return (
        logs.Panel()
        .datasource(loki_datasource_ref())
        .show_time(True)
        .sort_order(LogsSortOrder.DESCENDING)
        .enable_log_details(True)
    )


def loki_datasource_ref() -> DataSourceRef:
    """
    Returns a reference to the Loki datasource used by the
    workshop stack.
    """
    return DataSourceRef(type_val="loki", uid="loki")


def prometheus_datasource_ref() -> DataSourceRef:
    """
    Returns a reference to the Prometheus datasource used by the
    workshop stack.
    """
    return DataSourceRef(type_val="prometheus", uid="prometheus")


def loki_query(expression: str) -> loki.Dataquery:
    """
    Creates a Loki query pre-configured for range vectors.
    """
    return loki.Dataquery().expr(expression).query_type("range").legend_format("__auto")


def prometheus_query(expression: str) -> prometheus.Dataquery:
    """
    Creates a Prometheus query pre-configured for range vectors.
    """
    return (
        prometheus.Dataquery()
        .expr(expression)
        .range()
        .format(PromQueryFormat.TIME_SERIES)
        .legend_format("__auto")
    )


def instant_prometheus_query(expression: str) -> prometheus.Dataquery:
    """
    Creates a Prometheus query pre-configured for instant
    vectors and table data formatting.
    """
    return (
        prometheus.Dataquery()
        .expr(expression)
        .instant()
        .format(PromQueryFormat.TABLE)
        .legend_format("__auto")
    )

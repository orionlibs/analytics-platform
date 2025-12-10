from grafana_foundation_sdk.builders import common, logs, stat, text, timeseries
from grafana_foundation_sdk.models.common import (
    GraphDrawStyle,
    LegendDisplayMode,
    LegendPlacement,
    TooltipDisplayMode,
    StackingMode,
)
from grafana_foundation_sdk.models.dashboard import DynamicConfigValue

from .catalog import Service
from .common import (
    stat_panel,
    instant_prometheus_query,
    loki_datasource_ref,
    prometheus_datasource_ref,
    text_panel,
    loki_query,
    timeseries_panel,
)


def version_stat(service: Service) -> stat.Panel:
    return (
        stat_panel()
        .title("Version")
        .with_target(instant_prometheus_query('app_infos{service="%s"}' % service.name))
        .transparent(True)
        .datasource(prometheus_datasource_ref())
        .reduce_options(
            common.ReduceDataOptions()
            .values(False)
            .calcs(["last"])
            .fields("/^version$/")
        )
    )


def description_text(service: Service) -> text.Panel:
    return text_panel(service.description).transparent(True)


def logs_volume_timeseries(service: Service) -> timeseries.Panel:
    return (
        timeseries_panel()
        .title("Logs volume")
        .with_target(
            loki_query(
                'sum by (level) (count_over_time({service="%s", level=~"$logs_level"} |~ "$logs_filter" [$__auto]))'
                % service.name
            ).legend_format("{{ level }}")
        )
        .datasource(loki_datasource_ref())
        .stacking(common.StackingConfig().mode(StackingMode.NORMAL))
        .transparent(True)
        .tooltip(common.VizTooltipOptions().mode(TooltipDisplayMode.MULTI))
        .legend(
            common.VizLegendOptions()
            .display_mode(LegendDisplayMode.LIST)
            .placement(LegendPlacement.RIGHT)
            .show_legend(True)
        )
        .draw_style(GraphDrawStyle.BARS)
        .override_by_name(
            "INFO",
            [
                DynamicConfigValue(
                    id_val="color", value={"mode": "fixed", "fixedColor": "green"}
                ),
            ],
        )
        .override_by_name(
            "ERROR",
            [
                DynamicConfigValue(
                    id_val="color", value={"mode": "fixed", "fixedColor": "red"}
                ),
            ],
        )
    )

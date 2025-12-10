package main

import (
	"fmt"

	"github.com/grafana/grafana-foundation-sdk/go/common"
	"github.com/grafana/grafana-foundation-sdk/go/dashboard"
	"github.com/grafana/grafana-foundation-sdk/go/stat"
	"github.com/grafana/grafana-foundation-sdk/go/text"
	"github.com/grafana/grafana-foundation-sdk/go/timeseries"
)

func versionStat(service Service) *stat.PanelBuilder {
	return statPanel().
		Title("Version").
		WithTarget(
			instantPrometheusQuery(fmt.Sprintf("app_infos{service=\"%s\"}", service.Name)),
		).
		Transparent(true).
		Datasource(prometheusDatasourceRef()).
		ReduceOptions(common.NewReduceDataOptionsBuilder().
			Values(false).
			Calcs([]string{"last"}).
			Fields("/^version$/"),
		)
}

func descriptionText(service Service) *text.PanelBuilder {
	return textPanel(service.Description).
		Transparent(true)
}

func logsVolumeTimeseries(service Service) *timeseries.PanelBuilder {
	return timeseriesPanel().
		Title("Logs volume").
		WithTarget(
			lokiQuery(fmt.Sprintf("sum by (level) (count_over_time({service=\"%s\", level=~\"$logs_level\"} |~ \"$logs_filter\" [$__auto]))", service.Name)).
				LegendFormat("{{level}}"),
		).
		Stacking(common.NewStackingConfigBuilder().Mode(common.StackingModeNormal)).
		Transparent(true).
		Datasource(lokiDatasourceRef()).
		Tooltip(common.NewVizTooltipOptionsBuilder().Mode(common.TooltipDisplayModeMulti)).
		Legend(common.NewVizLegendOptionsBuilder().
			Placement(common.LegendPlacementRight).
			ShowLegend(true).
			DisplayMode(common.LegendDisplayModeList),
		).
		DrawStyle(common.GraphDrawStyleBars).
		OverrideByName("INFO", []dashboard.DynamicConfigValue{
			{
				Id:    "color",
				Value: map[string]any{"mode": "fixed", "fixedColor": "green"},
			},
		}).
		OverrideByName("ERROR", []dashboard.DynamicConfigValue{
			{
				Id:    "color",
				Value: map[string]any{"mode": "fixed", "fixedColor": "red"},
			},
		})
}

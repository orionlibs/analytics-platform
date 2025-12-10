import * as common from '@grafana/grafana-foundation-sdk/common';
import * as text from '@grafana/grafana-foundation-sdk/text';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';
import * as stat from '@grafana/grafana-foundation-sdk/stat';
import { Service } from './catalog';
import {
    instantPrometheusQuery,
    lokiDatasourceRef,
    lokiQuery,
    prometheusDatasourceRef,
    statPanel,
    textPanel,
    timeseriesPanel,
} from './common';

export const versionStat = (service: Service): stat.PanelBuilder => {
    return statPanel()
        .title('Version')
        .withTarget(
            instantPrometheusQuery(`app_infos{service="${service.name}"}`)
        )
        .transparent(true)
        .datasource(prometheusDatasourceRef())
        .reduceOptions(
            new common.ReduceDataOptionsBuilder()
                .values(false)
                .calcs(['last'])
                .fields('/^version$/')
        )
    ;
};

export const descriptionText = (service: Service): text.PanelBuilder => {
    return textPanel(service.description)
        .transparent(true)
    ;
};

export const logsVolumeTimeseries = (service: Service): timeseries.PanelBuilder => {
    return timeseriesPanel()
        .title('Logs volume')
        .withTarget(
            lokiQuery(`sum by (level) (count_over_time({service="${service.name}", level=~"$logs_level"} |~ "$logs_filter" [$__auto]))`)
                .legendFormat('{{ level }}')
        )
        .stacking(new common.StackingConfigBuilder().mode(common.StackingMode.Normal))
        .transparent(true)
        .datasource(lokiDatasourceRef())
        .tooltip(new common.VizTooltipOptionsBuilder().mode(common.TooltipDisplayMode.Multi))
        .legend(
            new common.VizLegendOptionsBuilder()
                .displayMode(common.LegendDisplayMode.List)
                .placement(common.LegendPlacement.Right)
                .showLegend(true)
        )
        .drawStyle(common.GraphDrawStyle.Bars)
        .overrideByName('INFO', [
            {id: 'color', value: {mode: 'fixed', fixedColor: 'green'}}
        ])
        .overrideByName('ERROR', [
            {id: 'color', value: {mode: 'fixed', fixedColor: 'red'}}
        ])
    ;
};
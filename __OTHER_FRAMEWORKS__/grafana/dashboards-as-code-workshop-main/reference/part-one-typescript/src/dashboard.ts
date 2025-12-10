import {
    DashboardBuilder,
    DashboardCursorSync,
} from '@grafana/grafana-foundation-sdk/dashboard';
import * as common from '@grafana/grafana-foundation-sdk/common';
import * as logs from '@grafana/grafana-foundation-sdk/logs';
import * as stat from '@grafana/grafana-foundation-sdk/stat';
import * as text from '@grafana/grafana-foundation-sdk/text';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';
import {
    instantPrometheusQuery,
    logPanel,
    lokiDatasourceRef,
    lokiQuery,
    prometheusDatasourceRef,
    prometheusQuery,
    statPanel,
    textPanel,
    timeseriesPanel
} from './common';

export const exampleDashboard = (): DashboardBuilder => {
    const builder = new DashboardBuilder(`Test dashboard`)
        .uid(`test-dashboard`)
        .tags(['test', 'generated'])
        .readonly()
        .tooltip(DashboardCursorSync.Crosshair)
        .refresh('10s')
        .time({ from: 'now-30m', to: 'now' })
    ;

    builder
        .withPanel(prometheusVersionStat())
        .withPanel(descriptionText())
        .withPanel(unfilteredLogs())
        .withPanel(prometheusGoroutinesTimeseries())
    ;

    return builder;
};

export const prometheusVersionStat = (): stat.PanelBuilder => {
    return statPanel()
        .title('Prometheus version')
        .withTarget(
            instantPrometheusQuery(`prometheus_build_info{}`)
        )
        .transparent(true)
        .datasource(prometheusDatasourceRef())
        .reduceOptions(
            new common.ReduceDataOptionsBuilder()
                .calcs(['last'])
                .fields('/^version$/')
        )
    ;
};

export const descriptionText = (): text.PanelBuilder => {
    return textPanel(`Text panels are supported too! Even with *markdown* text :)`)
        .transparent(true)
    ;
};

export const unfilteredLogs = (): logs.PanelBuilder => {
    return logPanel()
        .title('Logs')
        .withTarget(
            lokiQuery(`{job="app_logs"}`)
        )
        .datasource(lokiDatasourceRef())
    ;
};

export const prometheusGoroutinesTimeseries = (): timeseries.PanelBuilder => {
    return timeseriesPanel()
        .title('Prometheus goroutines')
        .withTarget(
            prometheusQuery(`go_goroutines{job="prometheus"}`)
        )
        .datasource(prometheusDatasourceRef())
    ;
};

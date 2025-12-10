import {
    DashboardBuilder,
    DashboardCursorSync,
} from '@grafana/grafana-foundation-sdk/dashboard';
import * as logs from '@grafana/grafana-foundation-sdk/logs';
import * as stat from '@grafana/grafana-foundation-sdk/stat';
import * as text from '@grafana/grafana-foundation-sdk/text';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';
import {
    logPanel,
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
        // TODO: configure the panel
        //
        //  * `title`: `Prometheus version`
        //  * `transparent` set to `true`
        //  * `reduce` options
        //    * `calcs` set to `["last"]`
        //    * `fields` set to `/^version$/`
        //  * Instant Prometheus query: `prometheus_build_info{}` (see common.instantPrometheusQuery())
        //  * `datasource`: Prometheus datasource ref (see common.prometheusDatasourceRef())
        //
        // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/Reference/stat/builder-PanelBuilder/
    ;
};

export const descriptionText = (): text.PanelBuilder => {
    return textPanel(``)
        // TODO: configure the panel
        //
        //  * `content`: `Text panels are supported too! Even with *markdown* text :)`
        //  * `transparent` set to `true`
        //
        // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/Reference/text/builder-PanelBuilder/
    ;
};

export const unfilteredLogs = (): logs.PanelBuilder => {
    return logPanel()
        // TODO: configure the panel
        //
        //  * `title`: `Logs`
        //  * Loki query: `{job="app_logs"}` (see common.lokiQuery())
        //  * `datasource`: loki datasource ref (see common.lokiDatasourceRef())
        //
        // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/Reference/logs/builder-PanelBuilder/
    ;
};

export const prometheusGoroutinesTimeseries = (): timeseries.PanelBuilder => {
    return timeseriesPanel()
        // TODO: configure the panel
        //
        //  * `title`: `Prometheus goroutines`
        //  * Prometheus query: `go_goroutines{job="prometheus"}` (see common.prometheusQuery())
        //  * `datasource`: prometheus datasource ref (see common.prometheusDatasourceRef())
        //
        // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/Reference/timeseries/builder-PanelBuilder/
    ;
};

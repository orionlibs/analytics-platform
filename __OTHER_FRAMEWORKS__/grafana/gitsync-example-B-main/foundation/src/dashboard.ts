import {
    DashboardBuilder,
    DashboardCursorSync,
} from '@grafana/grafana-foundation-sdk/dashboard';
import * as prometheus from '@grafana/grafana-foundation-sdk/prometheus';
import * as text from '@grafana/grafana-foundation-sdk/text';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';
import {
    prometheusDatasourceRef,
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
        .withPanel(grafanaGoroutinesTimeseries())
        .withPanel(descriptionText());

    return builder;  
};

export const grafanaGoroutinesTimeseries = (): timeseries.PanelBuilder => {
    const query = new prometheus.DataqueryBuilder()
            .expr(`go_goroutines{job="grafan"}`)
            .range()
            .format(prometheus.PromQueryFormat.TimeSeries)
            .legendFormat('__auto')

    return timeseriesPanel()
        .title('Grafana goroutines')
        .withTarget(query)
        .datasource(prometheusDatasourceRef())
    ;
};

export const descriptionText = (): text.PanelBuilder => {
    return textPanel(`Text panels are supported too! Even with *markdown* text :)`)
        .transparent(true)
    ;
};

import { DataSourceRef } from '@grafana/grafana-foundation-sdk/dashboard';
import * as common from '@grafana/grafana-foundation-sdk/common';
import * as logs from '@grafana/grafana-foundation-sdk/logs';
import * as loki from '@grafana/grafana-foundation-sdk/loki';
import * as prometheus from '@grafana/grafana-foundation-sdk/prometheus';
import * as stat from '@grafana/grafana-foundation-sdk/stat';
import * as text from '@grafana/grafana-foundation-sdk/text';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';

// This file contains a series of utility functions to simplify the creation
// of panels while providing a consistent "look and feel".

// Creates a pre-configured stat panel.
export const statPanel = (): stat.PanelBuilder => {
    return new stat.PanelBuilder();
};

// Creates a text panel pre-configured for markdown content.
export const textPanel = (content: string): text.PanelBuilder => {
    return new text.PanelBuilder()
        .mode(text.TextMode.Markdown)
        .content(content)
    ;
};

// Creates a pre-configured timeseries panel.
export const timeseriesPanel = (): timeseries.PanelBuilder => {
    return new timeseries.PanelBuilder()
        .fillOpacity(20)
        .gradientMode(common.GraphGradientMode.Opacity)
        .legend(
            new common.VizLegendOptionsBuilder()
                .displayMode(common.LegendDisplayMode.List)
                .placement(common.LegendPlacement.Bottom)
                .showLegend(true)
        )
    ;
};

// Creates a pre-configured logs panel.
export const logPanel = (): logs.PanelBuilder => {
    return new logs.PanelBuilder()
        .datasource(lokiDatasourceRef())
        .showTime(true)
        .sortOrder(common.LogsSortOrder.Descending)
        .enableLogDetails(true)
    ;
};

// Creates a Prometheus query pre-configured for range vectors.
export const prometheusQuery = (expression: string): prometheus.DataqueryBuilder => {
	return new prometheus.DataqueryBuilder()
        .expr(expression)
        .range()
        .format(prometheus.PromQueryFormat.TimeSeries)
        .legendFormat('__auto')
    ;
};

// Creates a Prometheus query pre-configured for instant vectors and table data
// formatting.
export const instantPrometheusQuery = (expression: string): prometheus.DataqueryBuilder => {
	return new prometheus.DataqueryBuilder()
        .expr(expression)
        .instant()
        .format(prometheus.PromQueryFormat.Table)
        .legendFormat('__auto')
    ;
};

// Creates a Loki query pre-configured for range vectors.
export const lokiQuery = (expression: string): loki.DataqueryBuilder => {
	return new loki.DataqueryBuilder()
        .expr(expression)
        .queryType('range')
        .legendFormat('__auto')
    ;
};

// Returns a reference to the Prometheus datasource used by the workshop stack.
export const prometheusDatasourceRef = (): DataSourceRef => {
	return {
		type: 'prometheus',
		uid:  'gdev-prometheus',
	};
};

// Returns a reference to the Loki datasource used by the workshop stack.
export const lokiDatasourceRef = (): DataSourceRef => {
	return {
		type: 'loki',
		uid:  'loki',
	};
};

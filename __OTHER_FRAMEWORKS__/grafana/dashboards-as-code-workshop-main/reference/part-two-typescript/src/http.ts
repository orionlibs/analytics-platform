import * as heatmap from '@grafana/grafana-foundation-sdk/heatmap';
import * as logs from '@grafana/grafana-foundation-sdk/logs';
import * as timeseries from '@grafana/grafana-foundation-sdk/timeseries';
import * as prometheus from '@grafana/grafana-foundation-sdk/prometheus';
import * as units from '@grafana/grafana-foundation-sdk/units';
import { Service } from './catalog';
import {
    heatmapPanel,
    logPanel,
    lokiQuery,
    prometheusDatasourceRef,
    prometheusQuery,
    timeseriesPanel,
} from './common';

export const httpRequestsTimeseries = (service: Service): timeseries.PanelBuilder => {
    return timeseriesPanel()
        .title('HTTP Requests')
        .unit(units.RequestsPerSecond)
        .withTarget(
            prometheusQuery(`rate(http_requests_total{service="${service.name}"}[$__rate_interval])`)
                .legendFormat('{{code}} - {{ method }} {{ path }}')
        )
        .datasource(prometheusDatasourceRef())
    ;
};

export const httpLatenciesHeatmap = (service: Service): heatmap.PanelBuilder => {
    return heatmapPanel()
        .title('HTTP Requests latencies')
        .withTarget(
            prometheusQuery(`sum(increase(http_requests_duration_seconds_bucket{service="${service.name}"}[$__rate_interval])) by (le)`)
                .format(prometheus.PromQueryFormat.Heatmap)
        )
        .datasource(prometheusDatasourceRef())
    ;
};

export const httpLogsPanel = (service: Service): logs.PanelBuilder => {
    return logPanel()
        .title('HTTP Logs')
        .withTarget(
            lokiQuery(`{service="${service.name}", source="http", level=~"$logs_level"} |~ "$logs_filter"`)
        )
    ;
};

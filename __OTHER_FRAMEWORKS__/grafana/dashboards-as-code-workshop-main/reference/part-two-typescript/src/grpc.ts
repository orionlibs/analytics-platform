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

export const grpcRequestsTimeseries = (service: Service): timeseries.PanelBuilder => {
    return timeseriesPanel()
        .title('gRPC Requests')
        .unit(units.RequestsPerSecond)
        .withTarget(
            prometheusQuery(`rate(grpc_server_handled_total{service="${service.name}"}[$__rate_interval])`)
                .legendFormat('{{ grpc_method }} – {{ grpc_code }}')
        )
        .datasource(prometheusDatasourceRef())
    ;
};

export const grpcLatenciesHeatmap = (service: Service): heatmap.PanelBuilder => {
    return heatmapPanel()
        .title('gRPC Requests latencies')
        .withTarget(
            prometheusQuery(`sum(increase(grpc_server_handling_seconds_bucket{service="${service.name}"}[$__rate_interval])) by (le)`)
                .format(prometheus.PromQueryFormat.Heatmap)
        )
        .datasource(prometheusDatasourceRef())
    ;
};

export const grpcLogsPanel = (service: Service): logs.PanelBuilder => {
    return logPanel()
        .title('gRPC Logs')
        .withTarget(
            lokiQuery(`{service="${service.name}", source="grpc", level=~"$logs_level"} |~ "$logs_filter"`)
        )
    ;
};

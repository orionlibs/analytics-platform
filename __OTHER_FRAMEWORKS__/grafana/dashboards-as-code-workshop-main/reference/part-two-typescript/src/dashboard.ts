import {
    DashboardBuilder,
    DashboardCursorSync,
    DashboardLinkBuilder,
    QueryVariableBuilder,
    RowBuilder,
    TextBoxVariableBuilder,
    VariableRefresh,
} from '@grafana/grafana-foundation-sdk/dashboard';
import { Service } from './catalog';
import { lokiDatasourceRef } from './common';
import { descriptionText, logsVolumeTimeseries, versionStat } from './overview';
import { grpcLatenciesHeatmap, grpcLogsPanel, grpcRequestsTimeseries } from './grpc';
import { httpLatenciesHeatmap, httpLogsPanel, httpRequestsTimeseries } from './http';

export const dashboardForService = (service: Service): DashboardBuilder => {
    const builder = new DashboardBuilder(`${service.name} service overview`)
        .uid(`${service.name}-overview`)
        .tags([service.name, 'generated'])
        .readonly()
        .tooltip(DashboardCursorSync.Crosshair)
        .refresh('10s')
        .time({ from: 'now-30m', to: 'now' })
        .link(
            new DashboardLinkBuilder('GitHub Repository')
                .url(service.github)
                .targetBlank(true)
        )
        .withVariable(new TextBoxVariableBuilder('logs_filter').label('Logs filter'))
        .withVariable(logLevelsVariable(service))
    ;

	// Overview
	builder
        .withPanel(versionStat(service).height(4).span(4))
        .withPanel(descriptionText(service).height(4).span(4))
        .withPanel(logsVolumeTimeseries(service).height(4).span(16))
    ;

	// gRPC row, if relevant
    if (service.has_grpc) {
        builder
            .withRow(new RowBuilder('gRPC'))
            .withPanel(grpcRequestsTimeseries(service).height(8))
            .withPanel(grpcLatenciesHeatmap(service).height(8))
            .withPanel(grpcLogsPanel(service).height(8).span(24))
        ;
    }

	// HTTP row, if relevant
    if (service.has_http) {
        builder
            .withRow(new RowBuilder('HTTP'))
            .withPanel(httpRequestsTimeseries(service).height(8))
            .withPanel(httpLatenciesHeatmap(service).height(8))
            .withPanel(httpLogsPanel(service).height(8).span(24))
        ;
    }

    return builder;
};

const logLevelsVariable = (service: Service): QueryVariableBuilder => {
    return new QueryVariableBuilder('logs_level')
        .label('Logs level')
        .datasource(lokiDatasourceRef())
        .query({
            type: 1,
            label: 'level',
            stream: `{service="${service.name}"}`,
        })
        .refresh(VariableRefresh.OnTimeRangeChanged)
        .includeAll(true)
        .allValue('.*');
};

package lab;

import com.grafana.foundation.common.*;
import com.grafana.foundation.dashboard.*;
import com.grafana.foundation.prometheus.PromQueryFormat;
import com.grafana.foundation.units.Constants;
import lab.catalog.Service;

import java.util.List;
import java.util.Map;

import static lab.Common.*;

public class Overview {
    public static DashboardBuilder forService(Service service) {
        DashboardBuilder builder = new DashboardBuilder(service.name+" service overview").
                uid(service.name+"-overview").
                tags(List.of("generated", service.name)).
                readonly().
                time(new DashboardDashboardTimeBuilder().
                        from("now-30m").
                        to("now")
                ).
                tooltip(DashboardCursorSync.CROSSHAIR).
                refresh("10s").
                link(new DashboardLinkBuilder("GitHub Repository").
                        url(service.repositoryUrl).
                        targetBlank(true)
                ).
                withVariable(new TextBoxVariableBuilder("logs_filter").
                        label("Logs filter")
                ).
                withVariable(logsLevelsVariable(service));

        // Overview
        builder.
                withPanel(versionStat(service).height(4).span(4)).
                withPanel(descriptionText(service).height(4).span(4)).
                withPanel(logsVolumeTimeseries(service).height(4).span(16));

        // gRPC row, if relevant
        if (service.hasGrpc) {
            builder.
                    withRow(new RowBuilder("gRPC")).
                    withPanel(grpcRequestsTimeseries(service).height(8)).
                    withPanel(grpcLatenciesHeatmap(service).height(8)).
                    withPanel(grpcLogs(service).height(8).span(24))
            ;
        }

        // HTTP row, if relevant
        if (service.hasHttp) {
            builder.
                    withRow(new RowBuilder("HTTP")).
                    withPanel(httpRequestsTimeseries(service).height(8)).
                    withPanel(httpLatenciesHeatmap(service).height(8)).
                    withPanel(httpLogs(service).height(8).span(24))
            ;
        }

        return builder;
    }

    private static com.grafana.foundation.stat.PanelBuilder versionStat(Service service) {
        return statPanel().
                title("Version").
                withTarget(
                        instantPrometheusQuery("app_infos{service=\""+service.name+"\"}")
                ).
                datasource(prometheusDatasourceRef()).
                transparent(true).
                reduceOptions(new ReduceDataOptionsBuilder().
                        calcs(List.of("last")).
                        fields("/^version$/")
                );
    }

    private static com.grafana.foundation.text.PanelBuilder descriptionText(Service service) {
        return textPanel(service.description).
                transparent(true);
    }

    private static com.grafana.foundation.timeseries.PanelBuilder logsVolumeTimeseries(Service service) {
        String query = "sum by (level) (count_over_time({service=\""+service.name+"\", level=~\"$logs_level\"} |~ \"$logs_filter\" [$__auto]))";

        return timeseriesPanel().
                title("Logs volume").
                withTarget(lokiQuery(query).legendFormat("{{ level }}")).
                stacking(new StackingConfigBuilder().mode(StackingMode.NORMAL)).
                transparent(true).
                datasource(lokiDatasourceRef()).
                tooltip(new VizTooltipOptionsBuilder().mode(TooltipDisplayMode.MULTI)).
                legend(new VizLegendOptionsBuilder().
                        displayMode(LegendDisplayMode.LIST).
                        placement(LegendPlacement.RIGHT).
                        showLegend(true)
                ).
                drawStyle(GraphDrawStyle.BARS).
                overrideByName("INFO", List.of(
                        new DynamicConfigValue("color", Map.of(
                                "mode", "fixed",
                                "fixedColor", "green"
                        ))
                )).
                overrideByName("ERROR", List.of(
                        new DynamicConfigValue("color", Map.of(
                                "mode", "fixed",
                                "fixedColor", "red"
                        ))
                ));
    }

    private static com.grafana.foundation.timeseries.PanelBuilder grpcRequestsTimeseries(Service service) {
        String query = "rate(grpc_server_handled_total{service=\""+service.name+"\"}[$__rate_interval])";

        return timeseriesPanel().
                title("gRPC Requests").
                unit(Constants.RequestsPerSecond).
                withTarget(prometheusQuery(query).legendFormat("{{ grpc_method }} – {{ grpc_code }}")).
                datasource(prometheusDatasourceRef());
    }

    private static com.grafana.foundation.heatmap.PanelBuilder grpcLatenciesHeatmap(Service service) {
        String query = "sum(increase(grpc_server_handling_seconds_bucket{service=\""+service.name+"\"}[$__rate_interval])) by (le)";

        return heatmapPanel().
                title("gRPC Requests latencies").
                withTarget(prometheusQuery(query).format(PromQueryFormat.HEATMAP)).
                datasource(prometheusDatasourceRef());
    }

    private static com.grafana.foundation.logs.PanelBuilder grpcLogs(Service service) {
        String query = "{service=\""+service.name+"\", source=\"grpc\", level=~\"$logs_level\"} |~ \"$logs_filter\"";

        return logPanel().
                title("gRPC Logs").
                withTarget(lokiQuery(query));
    }

    private static com.grafana.foundation.timeseries.PanelBuilder httpRequestsTimeseries(Service service) {
        String query = "rate(http_requests_total{service=\""+service.name+"\"}[$__rate_interval])";

        return timeseriesPanel().
                title("HTTP Requests").
                unit(Constants.RequestsPerSecond).
                withTarget(prometheusQuery(query).legendFormat("{{code}} – {{ method }} {{ path }}")).
                datasource(prometheusDatasourceRef());
    }

    private static com.grafana.foundation.heatmap.PanelBuilder httpLatenciesHeatmap(Service service) {
        String query = "sum(increase(http_requests_duration_seconds_bucket{service=\""+service.name+"\"}[$__rate_interval])) by (le)";

        return heatmapPanel().
                title("HTTP Requests latencies").
                withTarget(prometheusQuery(query).format(PromQueryFormat.HEATMAP)).
                datasource(prometheusDatasourceRef());
    }

    private static com.grafana.foundation.logs.PanelBuilder httpLogs(Service service) {
        String query = "{service=\""+service.name+"\", source=\"http\", level=~\"$logs_level\"} |~ \"$logs_filter\"";

        return logPanel().
                title("HTTP Logs").
                withTarget(lokiQuery(query));
    }

    private static QueryVariableBuilder logsLevelsVariable(Service service) {
        return new QueryVariableBuilder("logs_level").
                label("Logs level").
                datasource(lokiDatasourceRef()).
                query(StringOrMap.createMap(Map.of(
                        "label", "level",
                        "stream", "{service=\""+service.name+"\"}",
                        "type", 1
                ))).
                refresh(VariableRefresh.ON_TIME_RANGE_CHANGED).
                includeAll(true).
                allValue(".*");
    }
}

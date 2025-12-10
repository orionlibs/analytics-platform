<?php

namespace App\Dashboard;

use App\Catalog\Service;

use Grafana\Foundation\Common\GraphDrawStyle;
use Grafana\Foundation\Common\LegendDisplayMode;
use Grafana\Foundation\Common\LegendPlacement;
use Grafana\Foundation\Common\ReduceDataOptionsBuilder;
use Grafana\Foundation\Common\StackingConfigBuilder;
use Grafana\Foundation\Common\StackingMode;
use Grafana\Foundation\Common\TooltipDisplayMode;
use Grafana\Foundation\Common\VizLegendOptionsBuilder;
use Grafana\Foundation\Common\VizTooltipOptionsBuilder;
use Grafana\Foundation\Dashboard as SDKDashboard;
use Grafana\Foundation\Dashboard\DashboardBuilder;
use Grafana\Foundation\Dashboard\DashboardCursorSync;
use Grafana\Foundation\Dashboard\DashboardLinkBuilder;
use Grafana\Foundation\Dashboard\DynamicConfigValue;
use Grafana\Foundation\Dashboard\RowBuilder;
use Grafana\Foundation\Dashboard\TextBoxVariableBuilder;
use Grafana\Foundation\Dashboard\VariableRefresh;
use Grafana\Foundation\Heatmap;
use Grafana\Foundation\Logs;
use Grafana\Foundation\Prometheus\PromQueryFormat;
use Grafana\Foundation\Stat;
use Grafana\Foundation\Text;
use Grafana\Foundation\Timeseries;
use Grafana\Foundation\Units\Constants as Units;

class Overview
{
    public static function forService(Service $service): SDKDashboard\Dashboard
    {
        $builder = (new DashboardBuilder(title: $service->name.' service overview'))
            ->uid($service->name.'-overview')
            ->tags([$service->name, 'generated'])
            ->readonly()
            ->time('now-30m', 'now')
            ->tooltip(DashboardCursorSync::crosshair())
            ->refresh('10s')
            ->link(
                (new DashboardLinkBuilder('GitHub Repository'))
                    ->url($service->repositoryUrl)
                    ->targetBlank(true)
            )
            ->withVariable(
                (new TextBoxVariableBuilder('logs_filter'))
                    ->label('Logs filter')
            )
            ->withVariable(self::logLevelsVariable($service))
        ;

	    // Overview
        $builder
            ->withPanel(self::versionStat($service)->height(4)->span(4))
            ->withPanel(self::descriptionText($service)->height(4)->span(4))
            ->withPanel(self::logsVolumeTimeseries($service)->height(4)->span(16))
        ;

	    // gRPC row, if relevant
        if ($service->hasGrpc) {
            $builder
                ->withRow(new RowBuilder('gRPC'))
                ->withPanel(self::grpcRequestsTimeseries($service)->height(8))
                ->withPanel(self::grpcLatenciesHeatmap($service)->height(8))
                ->withPanel(self::grpcLogsPanel($service)->height(8)->span(24))
            ;
        }

	    // HTTP row, if relevant
        if ($service->hasHttp) {
            $builder
                ->withRow(new RowBuilder('HTTP'))
                ->withPanel(self::httpRequestsTimeseries($service)->height(8))
                ->withPanel(self::httpLatenciesHeatmap($service)->height(8))
                ->withPanel(self::httpLogsPanel($service)->height(8)->span(24))
            ;
        }

        return $builder->build();
    }

    private static function versionStat(Service $service): Stat\PanelBuilder
    {
        return Common::statPanel()
            ->title('Version')
            ->withTarget(
                Common::instantPrometheusQuery("app_infos{service=\"$service->name\"}")
            )
            ->transparent(true)
            ->datasource(Common::prometheusDatasourceRef())
            ->reduceOptions(
                (new ReduceDataOptionsBuilder())
                ->values(false)
                ->calcs(['last'])
                ->fields('/^version$/')
            )
        ;
    }

    private static function descriptionText(Service $service): Text\PanelBuilder
    {
        return Common::textPanel($service->description)
            ->transparent(true)
        ;
    }

    private static function logsVolumeTimeseries(Service $service): Timeseries\PanelBuilder
    {
        return Common::timeseriesPanel()
            ->title('Logs volume')
            ->withTarget(
                Common::lokiQuery("sum by (level) (count_over_time({service=\"$service->name\", level=~\"\$logs_level\"} |~ \"\$logs_filter\" [\$__auto]))")
                    ->legendFormat('{{ level }}')
            )
            ->stacking((new StackingConfigBuilder())->mode(StackingMode::normal()))
            ->transparent(true)
            ->datasource(Common::lokiDatasourceRef())
            ->tooltip((new VizTooltipOptionsBuilder())->mode(TooltipDisplayMode::multi()))
            ->legend(
                (new VizLegendOptionsBuilder())
                    ->displayMode(LegendDisplayMode::list())
                    ->placement(LegendPlacement::right())
                    ->showLegend(true)
            )
            ->drawStyle(GraphDrawStyle::bars())
            ->overrideByName('INFO', [
                new DynamicConfigValue('color', ['mode' => 'fixed', 'fixedColor' => 'green']),
            ])
            ->overrideByName('ERROR', [
                new DynamicConfigValue('color', ['mode' => 'fixed', 'fixedColor' => 'red']),
            ])
        ;
    }

    private static function grpcRequestsTimeseries(Service $service): Timeseries\PanelBuilder
    {
        return Common::timeseriesPanel()
            ->title('gRPC Requests')
            ->unit(Units::REQUESTS_PER_SECOND)
            ->withTarget(
                Common::prometheusQuery("rate(grpc_server_handled_total{service=\"$service->name\"}[\$__rate_interval])")
                    ->legendFormat('{{ grpc_method }} – {{ grpc_code }}')
            )
            ->datasource(Common::prometheusDatasourceRef())
        ;
    }

    private static function grpcLatenciesHeatmap(Service $service): Heatmap\PanelBuilder
    {
        return Common::heatmapPanel()
            ->title('gRPC Requests latencies')
            ->withTarget(
                Common::prometheusQuery("sum(increase(grpc_server_handling_seconds_bucket{service=\"$service->name\"}[\$__rate_interval])) by (le)")
                    ->format(PromQueryFormat::heatmap())
            )
            ->datasource(Common::prometheusDatasourceRef())
        ;
    }

    private static function grpcLogsPanel(Service $service): Logs\PanelBuilder
    {
        return Common::logPanel()
            ->title('gRPC Logs')
            ->withTarget(
                Common::lokiQuery("{service=\"$service->name\", source=\"grpc\", level=~\"\$logs_level\"} |~ \"\$logs_filter\"")
            )
        ;
    }

    private static function httpRequestsTimeseries(Service $service): Timeseries\PanelBuilder
    {
        return Common::timeseriesPanel()
            ->title('HTTP Requests')
            ->unit(Units::REQUESTS_PER_SECOND)
            ->withTarget(
                Common::prometheusQuery("rate(http_requests_total{service=\"$service->name\"}[\$__rate_interval])")
                    ->legendFormat('{{code}} – {{ method }} {{ path }}')
            )
            ->datasource(Common::prometheusDatasourceRef())
        ;
    }

    private static function httpLatenciesHeatmap(Service $service): Heatmap\PanelBuilder
    {
        return Common::heatmapPanel()
            ->title('HTTP Requests latencies')
            ->withTarget(
                Common::prometheusQuery("sum(increase(http_requests_duration_seconds_bucket{service=\"$service->name\"}[\$__rate_interval])) by (le)")
                    ->format(PromQueryFormat::heatmap())
            )
            ->datasource(Common::prometheusDatasourceRef())
        ;
    }

    private static function httpLogsPanel(Service $service): Logs\PanelBuilder
    {
        return Common::logPanel()
            ->title('HTTP Logs')
            ->withTarget(
                Common::lokiQuery("{service=\"$service->name\", source=\"http\", level=~\"\$logs_level\"} |~ \"\$logs_filter\"")
            )
        ;
    }

    private static function logLevelsVariable(Service $service): SDKDashboard\QueryVariableBuilder
    {
        return (new SDKDashboard\QueryVariableBuilder('logs_level'))
            ->label('Logs level')
            ->datasource(Common::lokiDatasourceRef())
            ->query([
				'label'  => 'level',
				'stream' => "{service=\"$service->name\"}",
				'type'   =>   1,
            ])
            ->refresh(VariableRefresh::onTimeRangeChanged())
            ->includeAll(true)
            ->allValue('.*')
        ;
    }
}

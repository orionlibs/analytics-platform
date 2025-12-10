<?php

namespace App\Dashboard;

use Grafana\Foundation\Common\GraphGradientMode;
use Grafana\Foundation\Common\LegendDisplayMode;
use Grafana\Foundation\Common\LegendPlacement;
use Grafana\Foundation\Common\LogsSortOrder;
use Grafana\Foundation\Common\ScaleDistribution;
use Grafana\Foundation\Common\ScaleDistributionConfigBuilder;
use Grafana\Foundation\Common\TooltipDisplayMode;
use Grafana\Foundation\Common\VizLegendOptionsBuilder;
use Grafana\Foundation\Dashboard\DataSourceRef;
use Grafana\Foundation\Heatmap;
use Grafana\Foundation\Heatmap\FilterValueRangeBuilder;
use Grafana\Foundation\Heatmap\HeatmapColorMode;
use Grafana\Foundation\Heatmap\HeatmapColorOptionsBuilder;
use Grafana\Foundation\Heatmap\HeatmapColorScale;
use Grafana\Foundation\Heatmap\YAxisConfigBuilder;
use Grafana\Foundation\Logs;
use Grafana\Foundation\Loki;
use Grafana\Foundation\Prometheus;
use Grafana\Foundation\Prometheus\PromQueryFormat;
use Grafana\Foundation\Stat;
use Grafana\Foundation\Text;
use Grafana\Foundation\Text\TextMode;
use Grafana\Foundation\Timeseries;

class Common
{
    public static function lokiDatasourceRef(): DataSourceRef
    {
        return new DataSourceRef(
            type: 'loki',
            uid: 'loki',
        );
    }

    public static function prometheusDatasourceRef(): DataSourceRef
    {
        return new DataSourceRef(
            type: 'prometheus',
            uid: 'prometheus',
        );
    }

    public static function statPanel(): Stat\PanelBuilder
    {
        return new Stat\PanelBuilder();
    }

    public static function heatmapPanel(): Heatmap\PanelBuilder
    {
        return (new Heatmap\PanelBuilder())
            ->color(
                (new HeatmapColorOptionsBuilder())
                ->mode(HeatmapColorMode::scheme())
                ->scheme('RdYlBu')
                ->scale(HeatmapColorScale::exponential())
                ->steps(64)
            )
            ->filterValues((new FilterValueRangeBuilder())->le(1e-09))
            ->yAxis((new YAxisConfigBuilder())->unit('s'))
            ->mode(TooltipDisplayMode::single())
            ->scaleDistribution((new ScaleDistributionConfigBuilder())->type(ScaleDistribution::linear()))
        ;
    }

    public static function logPanel(): Logs\PanelBuilder
    {
        return (new Logs\PanelBuilder())
            ->datasource(self::lokiDatasourceRef())
            ->showTime(true)
            ->sortOrder(LogsSortOrder::descending())
            ->enableLogDetails(true)
        ;
    }

    public static function textPanel(string $content): Text\PanelBuilder
    {
        return (new Text\PanelBuilder())
            ->mode(TextMode::markdown())
            ->content($content)
        ;
    }

    public static function timeseriesPanel(): Timeseries\PanelBuilder
    {
        return (new Timeseries\PanelBuilder())
            ->fillOpacity(20)
            ->gradientMode(GraphGradientMode::opacity())
            ->legend(
                (new VizLegendOptionsBuilder())
                    ->displayMode(LegendDisplayMode::list())
                    ->placement(LegendPlacement::bottom())
                    ->showLegend(true)
            )
        ;
    }

    public static function instantPrometheusQuery(string $expression): Prometheus\DataqueryBuilder
    {
        return (new Prometheus\DataqueryBuilder())
            ->expr($expression)
            ->instant()
            ->format(PromQueryFormat::table())
            ->legendFormat('__auto')
        ;
    }

    public static function prometheusQuery(string $expression): Prometheus\DataqueryBuilder
    {
        return (new Prometheus\DataqueryBuilder())
            ->expr($expression)
            ->range()
            ->format(PromQueryFormat::timeSeries())
            ->legendFormat('__auto')
        ;
    }

    public static function lokiQuery(string $expression): Loki\DataqueryBuilder
    {
        return (new Loki\DataqueryBuilder())
            ->expr($expression)
            ->QueryType('range')
            ->legendFormat('__auto')
        ;
    }
}
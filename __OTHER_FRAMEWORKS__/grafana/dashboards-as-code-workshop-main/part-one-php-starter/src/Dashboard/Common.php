<?php

namespace App\Dashboard;

use Grafana\Foundation\Dashboard\DataSourceRef;
use Grafana\Foundation\Logs;
use Grafana\Foundation\Loki;
use Grafana\Foundation\Prometheus;
use Grafana\Foundation\Prometheus\PromQueryFormat;
use Grafana\Foundation\Stat;
use Grafana\Foundation\Text;
use Grafana\Foundation\Timeseries;

class Common
{
    public static function statPanel(): Stat\PanelBuilder
    {
        // no specific options required for this lab.
        return new Stat\PanelBuilder();
    }

    public static function logPanel(): Logs\PanelBuilder
    {
        return (new Logs\PanelBuilder())
            // TODO: configure default options for logs panels
            //
            //  * `showTime` set to `true`
            //  * `sortOrder` set to `Descending`
            //  * `enableLogDetails` set to `true`
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/logs/builder-PanelBuilder/
        ;
    }

    public static function textPanel(string $content): Text\PanelBuilder
    {
        return (new Text\PanelBuilder())
            // TODO: configure default options for text panels
            //
            //  * `content` set to $content
            //  * `mode` set to `markdown`
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/text/builder-PanelBuilder/
        ;
    }

    public static function timeseriesPanel(): Timeseries\PanelBuilder
    {
        return (new Timeseries\PanelBuilder())
            // TODO: configure default options for timeseries panels
            //
            //  * `fillOpacity` set to `20`
            //  * `gradientMode` set to  `opacity`
            //  * `legend` options:
            //    * `displayMode` set to `list`
            //    * `placement` set to `bottom`
            //    * `showLegend` set to `true`
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/timeseries/builder-PanelBuilder/
        ;
    }

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

<?php

namespace App\Dashboard;

use Grafana\Foundation\Dashboard as SDKDashboard;
use Grafana\Foundation\Dashboard\DashboardBuilder;
use Grafana\Foundation\Dashboard\DashboardCursorSync;
use Grafana\Foundation\Logs;
use Grafana\Foundation\Stat;
use Grafana\Foundation\Text;
use Grafana\Foundation\Timeseries;

class Playground
{
    public static function create(): SDKDashboard\Dashboard
    {
        $builder = (new DashboardBuilder(title: 'Test dashboard'))
            ->uid('test-dashboard')
            ->tags(['test', 'generated'])
            ->readonly()
            ->time('now-30m', 'now')
            ->tooltip(DashboardCursorSync::crosshair())
            ->refresh('10s')
        ;

        $builder
            ->withPanel(self::prometheusVersionStat())
            ->withPanel(self::descriptionText())
            ->withPanel(self::unfilteredLogs())
            ->withPanel(self::prometheusGoroutinesTimeseries())
        ;

        return $builder->build();
    }

    private static function prometheusVersionStat(): Stat\PanelBuilder
    {
        return Common::statPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Prometheus version`
            //  * `transparent` set to `true`
            //  * `reduce` options
            //    * `calcs` set to `["last"]`
            //    * `fields` set to `/^version$/`
            //  * Instant Prometheus query: `prometheus_build_info{}` (see Common::instantPrometheusQuery())
            //  * `datasource`: Prometheus datasource ref (see Common::prometheusDatasourceRef())
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/stat/builder-PanelBuilder/
        ;
    }

    private static function descriptionText(): Text\PanelBuilder
    {
        return Common::textPanel('')
            // TODO: configure the panel
            //
            //  * `content`: `Text panels are supported too! Even with *markdown* text :)`
            //  * `transparent` set to `true`
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/text/builder-PanelBuilder/
        ;
    }

    private static function unfilteredLogs(): Logs\PanelBuilder
    {
        return Common::logPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Logs`
            //  * Loki query: `{job="app_logs"}` (see Common::lokiQuery())
            //  * `datasource`: loki datasource ref (see Common::lokiDatasourceRef() function)
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/logs/builder-PanelBuilder/
        ;
    }

    private static function prometheusGoroutinesTimeseries(): Timeseries\PanelBuilder
    {
        return Common::timeseriesPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Prometheus goroutines`
            //  * Prometheus query: `go_goroutines{job="prometheus"}` (see Common::prometheusQuery())
            //  * `datasource`: prometheus datasource ref (see Common::prometheusDatasourceRef())
            //
            // See: https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/timeseries/builder-PanelBuilder/
        ;
    }
}

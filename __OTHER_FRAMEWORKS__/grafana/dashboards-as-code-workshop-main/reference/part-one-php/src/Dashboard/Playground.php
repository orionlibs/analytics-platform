<?php

namespace App\Dashboard;

use Grafana\Foundation\Common\ReduceDataOptionsBuilder;
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
            ->title('Prometheus version')
            ->withTarget(
                Common::instantPrometheusQuery('prometheus_build_info{}')
            )
            ->transparent(true)
            ->datasource(Common::prometheusDatasourceRef())
            ->reduceOptions(
                (new ReduceDataOptionsBuilder())
                ->calcs(['last'])
                ->fields('/^version$/')
            )
        ;
    }

    private static function descriptionText(): Text\PanelBuilder
    {
        return Common::textPanel('Text panels are supported too! Even with *markdown* text :)')
            ->transparent(true)
        ;
    }

    private static function unfilteredLogs(): Logs\PanelBuilder
    {
        return Common::logPanel()
            ->title('Logs')
            ->datasource(Common::lokiDatasourceRef())
            ->withTarget(
                Common::lokiQuery('{job="app_logs"}')
            )
        ;
    }

    private static function prometheusGoroutinesTimeseries(): Timeseries\PanelBuilder
    {
        return Common::timeseriesPanel()
            ->title('Prometheus goroutines')
            ->withTarget(
                Common::prometheusQuery('go_goroutines{job="prometheus"}')
            )
            ->datasource(Common::prometheusDatasourceRef())
        ;
    }
}
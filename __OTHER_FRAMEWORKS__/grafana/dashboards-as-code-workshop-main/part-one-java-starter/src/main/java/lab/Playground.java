package lab;

import com.grafana.foundation.common.ReduceDataOptionsBuilder;
import com.grafana.foundation.dashboard.*;
import java.util.List;
import static lab.Common.*;

public class Playground {
    public static DashboardBuilder dashboard() {
        return new DashboardBuilder("Test dashboard").
                uid("test-dashboard").
                tags(List.of("generated", "test")).
                readonly().
                time(new DashboardDashboardTimeBuilder().
                        from("now-30m").
                        to("now")
                ).
                tooltip(DashboardCursorSync.CROSSHAIR).
                refresh("10s").
                withPanel(prometheusVersionStat()).
                withPanel(descriptionText()).
                withPanel(unfilteredLogs()).
                withPanel(prometheusGoroutinesTimeseries());
    }

    private static com.grafana.foundation.stat.PanelBuilder prometheusVersionStat() {
        return statPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Prometheus version`
            //  * `transparent` set to `true`
            //  * `reduce` options
            //    * `calcs` set to `["last"]`
            //    * `fields` set to `/^version$/`
            //  * Instant Prometheus query: `prometheus_build_info{}` (see Common::instantPrometheusQuery())
            //  * `datasource`: Prometheus datasource ref (see Common::prometheusDatasourceRef())
        ;
    }

    private static com.grafana.foundation.text.PanelBuilder descriptionText() {
        return textPanel("")
            // TODO: configure the panel
            //
            //  * `content`: `Text panels are supported too! Even with *markdown* text :)`
            //  * `transparent` set to `true`
        ;
    }

    private static com.grafana.foundation.logs.PanelBuilder unfilteredLogs() {
        return logPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Logs`
            //  * Loki query: `{job="app_logs"}` (see Common::lokiQuery())
            //  * `datasource`: loki datasource ref (see Common::lokiDatasourceRef() function)
        ;
    }

    private static com.grafana.foundation.timeseries.PanelBuilder prometheusGoroutinesTimeseries() {
        return timeseriesPanel()
            // TODO: configure the panel
            //
            //  * `title`: `Prometheus goroutines`
            //  * Prometheus query: `go_goroutines{job="prometheus"}` (see Common::prometheusQuery())
            //  * `datasource`: prometheus datasource ref (see Common::prometheusDatasourceRef())
        ;
    }
}

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
        return statPanel().
                title("Prometheus version").
                withTarget(
                        instantPrometheusQuery("prometheus_build_info{}")
                ).
                datasource(prometheusDatasourceRef()).
                transparent(true).
                reduceOptions(new ReduceDataOptionsBuilder().
                        calcs(List.of("last")).
                        fields("/^version$/")
                );
    }

    private static com.grafana.foundation.text.PanelBuilder descriptionText() {
        return textPanel("Text panels are supported too! Even with *markdown* text :)").
                transparent(true);
    }

    private static com.grafana.foundation.logs.PanelBuilder unfilteredLogs() {
        return logPanel().
                title("Logs").
                withTarget(lokiQuery("{job=\"app_logs\"}"));
    }

    private static com.grafana.foundation.timeseries.PanelBuilder prometheusGoroutinesTimeseries() {
        return timeseriesPanel().
                title("Prometheus goroutines").
                withTarget(prometheusQuery("go_goroutines{job=\"prometheus\"}")).
                datasource(prometheusDatasourceRef());
    }
}

package lab;

import com.grafana.foundation.common.*;
import com.grafana.foundation.dashboard.DataSourceRef;
import com.grafana.foundation.prometheus.PromQueryFormat;
import com.grafana.foundation.text.TextMode;

public class Common {
    public static com.grafana.foundation.stat.PanelBuilder statPanel() {
        // no specific options required for this lab.
        return new com.grafana.foundation.stat.PanelBuilder();
    }

    public static com.grafana.foundation.logs.PanelBuilder logPanel() {
        return new com.grafana.foundation.logs.PanelBuilder()
            // TODO: configure default options for logs panels
            //
            //  * `showTime` set to `true`
            //  * `sortOrder` set to `Descending`
            //  * `enableLogDetails` set to `true`
        ;
    }

    public static com.grafana.foundation.text.PanelBuilder textPanel(String content) {
        return new com.grafana.foundation.text.PanelBuilder()
            // TODO: configure default options for text panels
            //
            //  * `content` set to content
            //  * `mode` set to `markdown`
        ;
    }

    public static com.grafana.foundation.timeseries.PanelBuilder timeseriesPanel() {
        return new com.grafana.foundation.timeseries.PanelBuilder()
            // TODO: configure default options for timeseries panels
            //
            //  * `fillOpacity` set to `20`
            //  * `gradientMode` set to  `opacity`
            //  * `legend` options:
            //    * `displayMode` set to `list`
            //    * `placement` set to `bottom`
            //    * `showLegend` set to `true`
        ;
    }

    public static com.grafana.foundation.prometheus.DataqueryBuilder instantPrometheusQuery(String expression) {
        return new com.grafana.foundation.prometheus.DataqueryBuilder().
                expr(expression).
                instant().
                format(PromQueryFormat.TABLE).
                legendFormat("__auto");
    }

    public static com.grafana.foundation.prometheus.DataqueryBuilder prometheusQuery(String expression) {
        return new com.grafana.foundation.prometheus.DataqueryBuilder().
                expr(expression).
                range().
                format(PromQueryFormat.TIME_SERIES).
                legendFormat("__auto");
    }

    public static com.grafana.foundation.loki.DataqueryBuilder lokiQuery(String expression) {
        return new com.grafana.foundation.loki.DataqueryBuilder().
                expr(expression).
                queryType("range").
                legendFormat("__auto");
    }

    public static DataSourceRef prometheusDatasourceRef() {
        return new DataSourceRef("prometheus", "prometheus");
    }

    public static DataSourceRef lokiDatasourceRef() {
        return new DataSourceRef("loki", "loki");
    }
}

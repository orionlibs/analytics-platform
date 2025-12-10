package lab;

import com.grafana.foundation.common.*;
import com.grafana.foundation.dashboard.DataSourceRef;
import com.grafana.foundation.prometheus.PromQueryFormat;
import com.grafana.foundation.text.TextMode;

public class Common {
    public static DataSourceRef prometheusDatasourceRef() {
        return new DataSourceRef("prometheus", "prometheus");
    }

    public static DataSourceRef lokiDatasourceRef() {
        return new DataSourceRef("loki", "loki");
    }

    public static com.grafana.foundation.stat.PanelBuilder statPanel() {
        return new com.grafana.foundation.stat.PanelBuilder();
    }

    public static com.grafana.foundation.logs.PanelBuilder logPanel() {
        return new com.grafana.foundation.logs.PanelBuilder().
                datasource(lokiDatasourceRef()).
                showTime(true).
                sortOrder(LogsSortOrder.DESCENDING).
                enableLogDetails(true);
    }

    public static com.grafana.foundation.text.PanelBuilder textPanel(String content) {
        return new com.grafana.foundation.text.PanelBuilder().
                mode(TextMode.MARKDOWN).
                content(content);
    }

    public static com.grafana.foundation.timeseries.PanelBuilder timeseriesPanel() {
        return new com.grafana.foundation.timeseries.PanelBuilder().
                fillOpacity(20.0).
                legend(new VizLegendOptionsBuilder().
                        displayMode(LegendDisplayMode.LIST).
                        placement(LegendPlacement.BOTTOM).
                        showLegend(true)
                );
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
}

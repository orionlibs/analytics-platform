package lab.grafana;

import com.grafana.foundation.dashboard.Dashboard;
import com.grafana.foundation.resource.Metadata;

import java.util.Map;

public class Manifest {
    public static com.grafana.foundation.resource.Manifest dashboard(String folderUid, Dashboard dashboard) {
        Metadata meta = new Metadata();
        meta.name = dashboard.uid;
        meta.annotations = Map.of(
                "grafana.app/folder", folderUid
        );

        return new com.grafana.foundation.resource.Manifest(
                "dashboard.grafana.app/v1beta1",
                "Dashboard",
                meta,
                dashboard
        );
    }
}

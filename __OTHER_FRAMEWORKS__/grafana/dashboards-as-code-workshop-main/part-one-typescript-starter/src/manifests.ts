import { Dashboard } from "@grafana/grafana-foundation-sdk/dashboard";
import { Manifest } from "@grafana/grafana-foundation-sdk/resource";

export const dashboardManifest = (folderUid: string, dashboard: Dashboard): Manifest => {
    return {
        apiVersion: 'dashboard.grafana.app/v1beta1',
        kind: 'Dashboard',
        metadata: {
            annotations: {
                'grafana.app/folder': folderUid,
            },
            name: dashboard.uid!,
        },
        spec: dashboard,
    };
};

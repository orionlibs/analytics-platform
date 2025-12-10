The content of the Alloy config file in this directory is primarily based on [this page from the Garfana Docs site](https://grafana.com/docs/grafana-cloud/monitor-applications/application-observability/collector/grafana-alloy/#configure-alloy).

Some changes have been added; those additions have comments to help explain the differences.

If you want to make changes to this config, you can do the following:

- edit/save config.alloy (you could test it in a local Alloy instance at that point)
- rebuild the ConfigMap manifest:
```
kubectl create configmap --namespace collector alloy-config "--from-file=config.alloy=./config.alloy" --dry-run=client -o=yaml > demo-alloy-configmap.yaml
```
- then redeploy into the cluster.

For more info: see [Grafana Docs](https://grafana.com/docs/alloy/latest/configure/kubernetes/#method-2-create-a-separate-configmap-from-a-file).

## Prom-Rule-Stats-Exporter

This is a repo for you to track individual rule performance over time rather the default of per rule-group.

#### Configuration

| Env Variables     | Flag      | Description                                                                                                   |
| ----------------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| ___ | `--http.listen-address` | Address to listen on for scrapes.                                                              |
| PROMETHEUS_ADDRESS    | `--prometheus.address` | Address to query Prometheus server on.                                                              |
| PROMETHEUS_USER    | `--prometheus.user`   |  Basic auth user. If you're using GrafanaCloud this is your instance ID. |
| PROMETHEUS_PASSWORD    | `--prometheus.password`   |  Basic auth password. If you're using GrafanaCloud this is your API Key. |

#### Running the command

```
./prom-rule-stats-exporter --prometheus.address=https://prometheus-us-central1.grafana.net/api/prom --prometheus.user=<1234> --prometheus.password=<API-Key> --log.level=debug
```
# Grafana Agent Buildpack

This is a buildpack for
[Grafana Agent](https://github.com/grafana/agent) deployments.

## Usage

### Config
Your config file should be placed into the root as `config.yml`.

The buildpack will substitute any environment variables. Example:

```yaml
---
server:
  http_listen_port: $PORT

prometheus:
  wal_directory: "./"
  global:
    scrape_interval: 5s
  configs:
    - name: agent
      host_filter: false
      scrape_configs:
        - job_name: taylor-swift-metrics
          metrics_path: /metrics
          scheme: https
          static_configs:
            - targets: ['target.taysway.xyz']
      remote_write:
        - url: https://prom.taysway.xyz/api/prom/push
          basic_auth:
            username: $USERNAME
            password: $PASSWORD
```


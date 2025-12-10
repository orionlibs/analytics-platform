# Snyk exporter

[![Build Status](https://travis-ci.com/lunarway/snyk_exporter.svg?branch=master)](https://travis-ci.com/lunarway/snyk_exporter)
[![Go Report Card](https://goreportcard.com/badge/github.com/lunarway/snyk_exporter)](https://goreportcard.com/report/github.com/lunarway/snyk_exporter)
[![Docker Repository on Quay](https://quay.io/repository/lunarway/snyk_exporter/status "Docker Repository on Quay")](https://quay.io/repository/lunarway/snyk_exporter)

Prometheus exporter for [Snyk](https://snyk.io/) written in Go. Allows for
exporting scanning data into Prometheus by scraping the Snyk HTTP API.

## Installation

Several pre-compiled binaries are available from the [releases
page](https://github.com/lunarway/snyk_exporter/releases).

A Docker image is also available on our Quay.io registry.

```shell
docker run grafana/snyk_exporter:latest --snyk.api-token '<api-token>'
```

## Usage

You need a Snyk API token to access to API. Get your through the [Snyk account
settings](https://app.snyk.io/account/).

It exposes prometheus metrics on `/metrics` on port `9532` (can be configured).

```shell
snyk_exporter --snyk.api-token '<api-token>'
```

See all configuration options with the `--help` flag

```text
$ snyk_exporter --help
usage: snyk_exporter --snyk.api-token=SNYK.API-TOKEN [<flags>]

Snyk exporter for Prometheus. Provide your Snyk API token and the organization(s) to scrape to
expose Prometheus metrics.

Flags:
  -h, --help               Show context-sensitive help (also try --help-long and --help-man).
      --snyk.api-url="https://snyk.io/api/v1"
                           Snyk API URL (legacy)
      --snyk.rest-api-url="https://api.snyk.io/rest"
                           Snyk REST API URL
      --snyk.rest-api-version="2023-06-22"
                           Snyk REST API Version
      --snyk.api-token=SNYK.API-TOKEN
                           Snyk API token
  -i, --snyk.interval=600  Polling interval for requesting data from Snyk API in seconds
      --snyk.organization=SNYK.ORGANIZATION ...
                           Snyk organization ID to scrape projects from (can be repeated for
                           multiple organizations)
      --snyk.target=SNYK.TARGET ...
                           Snyk target/repo name to scrape projects from (can be repeated for
                           multiple targets)
      --snyk.origin=SNYK.ORIGIN ...
                           Snyk project origin (can be repeated for multiple origins)
      --snyk.project-filter=SNYK.PROJECT-FILTER
                           Project filter (e.g. attributes.imageCluster=mycluster).
      --snyk.timeout=10    Timeout for requests against Snyk API
      --web.listen-address=":9532"
                           Address on which to expose metrics.
      --log.level="info"   Only log messages with the given severity or above. Valid levels:
                           [debug, info, warn, error, fatal]
      --log.format="logger:stderr"
                           Set the log target and format. Example:
                           "logger:syslog?appname=bob&local=7" or "logger:stdout?json=true"
      --version            Show application version.
```

It is possible to use a file to pass arguments to the exporter. For example:

```shell
echo '--snyk.api-token=<api-token>' > args
```

And run the exporter using:

```shell
./snyk-exporter @args
```

## Design

The exporter starts a long-running go routine on startup that scrapes the Snyk
API with a fixed interval (default every `10` minutes). The interval can be
configured as needed.

The API results are aggregated and recorded on the `snyk_vulnerabilities_total`
metric with the following labels:

- `organization` - The organization where the vulnerable project exists
- `target` - The target/repo name of the vulnerable project
- `project` - The project with a vulnerability
- `project_type` - The type of the project (`npm`, `maven`, `rubygems`, etc.)
- `severity` - The severity of the vulnerability, can be `critical`, `high`, `medium` and `low`
- `issue_type` - The type of issue, e.g. `vuln`, `license`
- `issue_title` - The issue title of the vulnerability, e.g. `Denial os Service
  (DoS)`. Can be the CVE if the vulnerability is not named by Snyk
- `ignored` - The issue is ignored in Snyk.
- `upgradeable` - The issue can be fixed by upgrading to a later version of the dependency.
- `patchable` - The issue is patchable through Snyk.
- `monitored` - The project is actively monitored by Snyk.

Here is an example.

```text
snyk_vulnerabilities_total{organization="my-org",target="my-scm-org/repo",project="my-app",project_type="npm",severity="critical",issue_type="vuln",issue_title="Remote Code Execution",ignored="false",upgradeable="false",patchable="false",monitored="true"} 1.0
snyk_vulnerabilities_total{organization="my-org",target="my-scm-org/repo",project="my-app",project_type="npm",severity="high",issue_type="vuln",issue_title="Privilege Escalation",ignored="false",upgradeable="false",patchable="false",monitored="true"} 1.0
snyk_vulnerabilities_total{organization="my-org",target="my-scm-org/repo",project="my-app",project_type="npm",severity="low",issue_type="vuln",issue_title="Sandbox (chroot) Escape",ignored="true",upgradeable="false",patchable="false",monitored="false"} 2.0
snyk_vulnerabilities_total{organization="my-org",target="my-scm-org/repo",project="my-app",project_type="npm",severity="medium",issue_type="license",issue_title="MPL-2.0 license",ignored="true",upgradeable="false",patchable="false",monitored="true"} 1
```

## Build

The exporter can be build using the standard Go tool chain if you have it
available.

```shell
go build
```

You can build inside a Docker image as well. This produces a `snyk_exporter`
image that can run with the binary as entry point.

```shell
docker build -t snyk_exporter .
```

This is useful if the exporter is to be depoyled in Kubernetes or other
dockerized environments.

Here is an example of running the exporter locally.

```shell
docker run -p9532:9532 snyk_exporter --snyk.api-token <api-token>
```

## Deployment

To deploy the exporter in Kubernetes, you can find a simple Kubernetes deployment
and secret yaml in the `examples` folder. You have to add your Snyk token in the
`secrets.yaml` and/or the snyk organizations that you want to get metrics from in
the args section of the `deployment.yaml`. If you don't specify a
snyk-organization, the exporter will scrape all organizations the token provides
access to. The examples assumes that you have a namespace in Kubernetes named:
`monitoring`.

It further assumes that you have [kubernetes service discovery](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config) configured for you Prometheus instance and a target that will gather metrics from pods, similar to this:

```yaml
- job_name: 'kubernetes-pods'
  kubernetes_sd_configs:
  - role: pod

  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    action: keep
    regex: true
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    action: replace
    target_label: __metrics_path__
    regex: (.+)
  - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
    action: replace
    regex: (.+):(?:\d+);(\d+)
    replacement: ${1}:${2}
    target_label: __address__
  - action: labelmap
    regex: __meta_kubernetes_pod_label_(.+)
```

To deploy it to your kubernetes cluster run the following commands:

```shell
kubectl apply -f examples/secrets.yaml
kubectl apply -f examples/deployment.yaml
```

The exporter expose http endpoints that can be used by kubernetes probes:

- `/healthz` - used for liveness probe, always returns `healthy`, status code 200.
- `/ready` - used for readiness probe, return `true` and status code 200 after
  the first scrape completed. Otherwise, it returns `false`, with status code 503.

## Development

The project uses Go modules so you need Go version >=1.11 to run it. Run builds
and tests with the standard Go tool chain.

```go
go build
go test
```

## Credits

This exporter is written with inspiration from
[dnanexus/prometheus_snyk_exporter](https://github.com/dnanexus/prometheus_snyk_exporter).

Main difference is the aggregations are done by Prometheus instead of in the
exporter. It also scrapes the Snyk API asyncronously, ie. not when Prometheus
tries to scrape the metrics.

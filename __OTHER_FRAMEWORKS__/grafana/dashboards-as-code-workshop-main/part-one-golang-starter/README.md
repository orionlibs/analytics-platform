# Hands-on lab — Grafana as code: Build and deploy your dashboards at scale

## Installing dependencies

```shell
go mod tidy
go mod vendor
```

## Running the code

```shell
go run .
```

It will generate a single dashboard and print its representation to stdout.
This mode is meant for development, to be used alongside `grafanactl`:

```shell
grafanactl resources serve --script 'go run .' --watch .
```

## Where should I start?

The [`main.go`](./main.go) file is the entrypoint both for the development and
deployment *modes*.

The [`dashboard.go`](./dashboard.go) file defines a `testDashboard()`
function that will be called to generate the dashboard.

The [`common.go`](./common.go) file is where "base functions" for each panel type should be defined.

> [!TIP]
> It is highly recommended that every panel created for your dashboard use one
> of these utility functions.

## Deploying the dashboards

```shell
go run . -manifests
```

This will generate a YAML manifest for the test dashboard.
The manifest is written under `./resources/` by default and can be deployed
from the CLI:

```shell
grafanactl resources push
```

## Useful resources

* [Example dashboards](https://github.com/grafana/grafana-foundation-sdk/tree/main/examples/go) built with the Foundation SDK
* [Foundation SDK how-to guides](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/go/How-To/building-a-dashboard/)
* [Foundation SDK reference](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/go/Reference/)

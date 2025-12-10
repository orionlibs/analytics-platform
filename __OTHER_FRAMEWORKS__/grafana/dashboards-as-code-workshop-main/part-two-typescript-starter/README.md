# Hands-on lab — Grafana as code: Build and deploy your dashboards at scale

## Installing dependencies

```shell
yarn install
```

## Running the code

```shell
yarn dev
```

It will generate a single dashboard, with a hardcoded service configuration.
This mode is meant for development, to be used alongside `grafanactl`:

```shell
grafanactl resources serve --script 'yarn -s dev' --watch .
```

## Where should I start?

The [`./src/index.ts`](./src/index.ts) file is the entrypoint both for the development and
deployment *modes*.

The [`./src/dashboard.ts`](./src/dashboard.ts) file defines a `dashboardForService()`
function that will be called to generate a dashboard for a given service.

The [`./src/common.ts`](./src/common.ts) file contains a few utilities related
to panel creations with sensible defaults and configuration.

> [!TIP]
> It is highly recommended that every panel created for your dashboard use one
> of these utility functions.

## Deploying the dashboards

```shell
yarn dev --manifests
```

This will call the service catalog and generate a dashboard manifest for each
service it describes.
These manifests are written under `./resources/` and can be deployed from the CLI:

```shell
grafanactl resources push
```

## Useful resources

* [Example dashboards](https://github.com/grafana/grafana-foundation-sdk/tree/main/examples/typescript) built with the Foundation SDK
* [Foundation SDK how-to guides](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/How-To/building-a-dashboard/)
* [Foundation SDK reference](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/typescript/Reference/)

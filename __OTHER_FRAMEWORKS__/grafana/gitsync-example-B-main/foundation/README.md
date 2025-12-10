# Hands-on lab: Grafana as code

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

The [`./src/dashboard.ts`](./src/dashboard.ts) file defines a `exampleDashboard()`
function that will be called to generate the dashboard.

The [`./src/common.ts`](./src/common.ts) file is where "base functions" for each panel type should be defined.

> [!TIP]
> It is highly recommended that every panel created for your dashboard use one
> of these utility functions.

## Deploying the dashboards

```shell
yarn dev --manifests
```

This will generate a YAML manifest for the test dashboard.
The manifest is written under `./manifests/` by default and can be deployed
from the CLI:

```shell
grafanactl resources push -d ./manifests
```
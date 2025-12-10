# Hands-on lab — Grafana as code: Build and deploy your dashboards at scale

## Installing dependencies

```shell
composer install
```

## Running the code

```shell
php index.php
```

It will generate a single dashboard, with a hardcoded service configuration.
This mode is meant for development, to be used alongside `grafanactl`:

```shell
grafanactl resources serve --script 'php index.php' --watch .
```

## Where should I start?

The [`index.php`](./index.php) file is the entrypoint both for the development and
deployment *modes*.

The [`./src/Dashboard/Playground.php`](./src/Dashboard/Playground.php) file defines a `Playground::create()`
static method that will be called to generate the dashboard.

The [`./src/Dashboard/Common.php`](./src/Dashboard/Common.php) file is where "base functions" for each panel type should be defined.

> [!TIP]
> It is highly recommended that every panel created for your dashboard use one
> of these utility functions.

## Deploying the dashboards

```shell
php index.php --manifests
```

This will generate a YAML manifest for the test dashboard.
The manifest is written under `./resources/` by default and can be deployed
from the CLI:

```shell
grafanactl resources push
```

## Useful resources

* [Example dashboards](https://github.com/grafana/grafana-foundation-sdk/tree/main/examples/php) built with the Foundation SDK
* [Foundation SDK how-to guides](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/How-To/building-a-dashboard/)
* [Foundation SDK reference](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/)

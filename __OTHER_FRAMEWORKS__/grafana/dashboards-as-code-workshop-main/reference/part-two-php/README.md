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

The [`./src/Dashboard/Overview.php`](./src/Dashboard/Overview.php) file defines a `Overview::forService()`
static method that will be called to generate a dashboard for a given service.

The [`./src/Dashboard/Common.php`](./src/Dashboard/Common.php) file contains a few utilities related
to panel creations with sensible defaults and configuration.

> [!TIP]
> It is highly recommended that every panel created for your dashboard use one
> of these utility functions.

## Deploying the dashboards

```shell
php index.php --manifests
```

This will call the service catalog and generate a dashboard manifest for each
service it describes.
These manifests are written under `./resources/` by default and can be deployed
from the CLI:

```shell
grafanactl resources push
```

## Useful resources

* [Example dashboards](https://github.com/grafana/grafana-foundation-sdk/tree/main/examples/php) built with the Foundation SDK
* [Foundation SDK how-to guides](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/How-To/building-a-dashboard/)
* [Foundation SDK reference](https://grafana.github.io/grafana-foundation-sdk/v11.6.x+cog-v0.0.x/php/Reference/)

# Concepts

The Grafana Foundation SDK is library for manipulating and generating Grafana resources – dashboards, alerts, … – as-code, in various languages.

Instead of having to deal with massive JSON blobs that model Grafana resources (ex: [Dashboard JSON Model](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/)),
compose resources in the language of your choice:

* Go
* Java
* PHP
* Python
* Typescript

For each language, the SDK provides **types** representing various resources.

**Builders** are the go-to objects when composing resources. They expose a
strongly-typed API, guiding you through the creation process.
Each builder is responsible for a single resource type and exposes **options**
specific to it.

Explore [the SDK's documentation](https://grafana.github.io/grafana-foundation-sdk/)
to learn more about the supported resource types and their options.

## Next steps

[Part one](./part-one.md)

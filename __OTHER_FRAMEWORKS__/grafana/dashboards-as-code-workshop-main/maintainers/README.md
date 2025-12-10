# Notes

## Starting the stack

```console
docker compose -f docker-compose.yaml up --watch --build
```

`--watch` will watch for changes in `./dummy/` and `./service-catalog`, and rebuild+restart the services when needed.

The Grafana instance is accessible at `http://localhost:3000` (anonymous usage is enabled)

## Service catalog

The fake service catalog is implemented as a small Go application serving a static JSON file (the catalog)
over HTTP.

Code: `./service-catalog`

Catalog endpoint: `http://localhost:8082/api/services`

## Fake services

Fake services are implemented by a single Go application which randomly emits metrics and logs.

Code: `./dummy`

The metrics emitted for each service can somewhat be configured. See the [`./dummy/services.go`](./dummy/services.go) file

## Exporting docker images for offline use

In case WiFi goes down or the Docker registry can't be accessed for some reason (ie: down, rate-limits, ...), the images
used by the lab can be exported and shared with attendees via a USB stick:

```shell
./export-docker-images.sh
```

This script relies on [`docker save`](https://docs.docker.com/reference/cli/docker/image/save/) to create tarballs of the images
referenced in the `docker-compose.yaml` file.

They can then be loaded via [`docker load`](https://docs.docker.com/reference/cli/docker/image/load/).

```shell
docker load --input prometheus.tar
```

## Running a docker registry locally

```shell
docker run -p 5000:5000 --restart always -v $(pwd)/registry-data:/var/lib/registry registry:3.0.0
```

A script is provided to push every image used by the lab:

```shell
./push-images-to-local-registry.sh
```

The registry used by `docker compose` commands can be overridden by setting the `REGISTRY` environment variable:

```shell
REGISTRY='host:5000` docker compose up
```

import argparse
import os
import sys

from grafana_foundation_sdk.cog.encoder import JSONEncoder

from src.catalog import Config as CatalogConfig, Client as Catalog, Service
from src.dashboard import dashboard_for_service
from src.grafana import Config as GrafanaConfig, Client as Grafana
from src.manifests import Manifest


MANIFESTS_DIR = "./resources"


def print_development_dashboard():
    service = Service(
        name="products",
        description="A service related to products",
        has_http=True,
        has_grpc=True,
        repository_url="http://github.com/org/products-service",
    )

    dashboard = dashboard_for_service(service)
    manifest = Manifest.dashboard("", dashboard.build())
    print(JSONEncoder(sort_keys=True, indent=2).encode(manifest))


def fetch_services_and_deploy():
    catalog = Catalog(CatalogConfig.from_env())
    grafana = Grafana(GrafanaConfig.from_env())
    services = catalog.services()

    for service in services:
        dashboard = dashboard_for_service(service)
        folder_uid = grafana.find_or_create_folder(service.name)

        grafana.persist_dashboard(folder_uid, dashboard.build())

    print(f"{len(services)} dashboards deployed")


def fetch_services_and_generate_manifests():
    catalog = Catalog(CatalogConfig.from_env())
    grafana = Grafana(GrafanaConfig.from_env())
    services = catalog.services()

    if not os.path.exists(MANIFESTS_DIR):
        os.mkdir(MANIFESTS_DIR)

    for service in services:
        dashboard = dashboard_for_service(service).build()
        folder_uid = grafana.find_or_create_folder(service.name)

        manifest = Manifest.dashboard(folder_uid, dashboard)

        filepath = os.path.join(MANIFESTS_DIR, f"{dashboard.uid}.json")
        with open(filepath, "w") as file:
            file.write(JSONEncoder(sort_keys=True, indent=2).encode(manifest))

    print(f"{len(services)} manifests generated in {MANIFESTS_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="part-two")
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Fetch the list of services from the catalog and deploy a dashboard for each entry",
    )
    parser.add_argument(
        "--manifests",
        action="store_true",
        help="Fetch the list of services from the catalog and generate a dashboard manifest for each entry",
    )

    args = parser.parse_args()

    # Fetch the list services from the catalog and deploy a dashboard for each
    # of them.
    if args.deploy:
        fetch_services_and_deploy()
        sys.exit(0)

    # Fetch the list services from the catalog and generate a dashboard manifest
    # for each of them.
    if args.manifests:
        fetch_services_and_generate_manifests()
        sys.exit(0)

    # Assume we're in "development mode" and print a single dashboard to stdout
    print_development_dashboard()

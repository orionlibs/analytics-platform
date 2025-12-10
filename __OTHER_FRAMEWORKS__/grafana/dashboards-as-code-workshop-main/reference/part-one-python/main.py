import argparse
import os
import sys

from grafana_foundation_sdk.builders import dashboard
from grafana_foundation_sdk.cog.encoder import JSONEncoder

from src.dashboard import example_dashboard
from src.grafana import Config as GrafanaConfig, Client as Grafana
from src.manifests import Manifest


MANIFESTS_DIR = "./resources"
DASHBOARD_FOLDER_NAME = "Part one"


def deploy_dashboard(dash_builder: dashboard.Dashboard):
    grafana = Grafana(GrafanaConfig.from_env())

    folder_uid = grafana.find_or_create_folder(DASHBOARD_FOLDER_NAME)
    grafana.persist_dashboard(folder_uid, dash_builder.build())

    print("dashboards deployed")


def generate_manifests(dash_builder: dashboard.Dashboard):
    grafana = Grafana(GrafanaConfig.from_env())
    dash = dash_builder.build()

    if not os.path.exists(MANIFESTS_DIR):
        os.mkdir(MANIFESTS_DIR)

    folder_uid = grafana.find_or_create_folder(DASHBOARD_FOLDER_NAME)
    manifest = Manifest.dashboard(folder_uid, dash)

    filepath = os.path.join(MANIFESTS_DIR, f"{dash.uid}.json")
    with open(filepath, "w") as file:
        file.write(JSONEncoder(sort_keys=True, indent=2).encode(manifest))

    print(f"manifests generated in {MANIFESTS_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="part-two")
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Generate and deploy the test dashboard directly to a Grafana instance",
    )
    parser.add_argument(
        "--manifests",
        action="store_true",
        help="Generate a dashboard manifest for the test dashboard and write it to disk",
    )

    args = parser.parse_args()

    dash = example_dashboard()

    # Deploy the test dashboard directly to a Grafana instance
    if args.deploy:
        deploy_dashboard(dash)
        sys.exit(0)

    # Generate a dashboard manifest for the test dashboard and write it to disk
    if args.manifests:
        generate_manifests(dash)
        sys.exit(0)

    # Assume we're in "development mode" and print a single dashboard to stdout
    manifest = Manifest.dashboard("", dash.build())
    print(JSONEncoder(sort_keys=True, indent=2).encode(manifest))

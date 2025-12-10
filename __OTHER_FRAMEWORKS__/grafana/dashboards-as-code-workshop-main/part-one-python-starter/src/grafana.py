import urllib.parse
import json
import os
import typing
import requests
from grafana_foundation_sdk.models.dashboard import Dashboard
from grafana_foundation_sdk.cog.encoder import JSONEncoder


class Config:
    host: str
    user: str
    password: str

    def __init__(self, host: str = "", user: str = "", password: str = ""):
        self.host = host
        self.user = user
        self.password = password

    @classmethod
    def from_env(cls) -> typing.Self:
        return cls(
            host=os.environ.get("GRAFANA_HOST", "localhost:3000"),
            user=os.environ.get("GRAFANA_USER", "admin"),
            password=os.environ.get("GRAFANA_PASSWORD", "admin"),
        )


class Client:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def find_or_create_folder(self, name: str) -> str:
        auth = (self.config.user, self.config.password)
        response = requests.get(
            f"http://{self.config.host}/api/search?type=dash-folder&query={urllib.parse.quote_plus(name)}",
            auth=auth,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"could not fetch folders list: expected 200, got {response.status_code}"
            )

        # The folder exists.
        response_json = response.json()
        if len(response_json) == 1:
            return response_json[0]["uid"]

        # The folder doesn't exist: we create it.
        response = requests.post(
            f"http://{self.config.host}/api/folders",
            auth=auth,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"title": name}),
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"could not create new folder: expected 200, got {response.status_code}"
            )

        return response.json()["uid"]

    def persist_dashboard(self, folder_uid: str, dashboard: Dashboard):
        auth = (self.config.user, self.config.password)
        response = requests.post(
            f"http://{self.config.host}/api/dashboards/db",
            auth=auth,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "dashboard": dashboard,
                    "folderUid": folder_uid,
                    "overwrite": True,
                },
                cls=JSONEncoder,
            ),
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"could not persist dashboard: expected 200, got {response.status_code}"
            )

import os
import requests
import typing


class Service:
    name: str
    description: str
    has_http: bool
    has_grpc: bool
    repository_url: str

    def __init__(
        self,
        name: str = "",
        description: str = "",
        has_http: bool = False,
        has_grpc: bool = False,
        repository_url: str = "",
    ):
        self.name = name
        self.description = description
        self.has_http = has_http
        self.has_grpc = has_grpc
        self.repository_url = repository_url

    @classmethod
    def from_json(cls, data: dict[str, typing.Any]) -> typing.Self:
        args: dict[str, typing.Any] = {}

        if "name" in data:
            args["name"] = data["name"]
        if "description" in data:
            args["description"] = data["description"]
        if "has_http" in data:
            args["has_http"] = data["has_http"]
        if "has_grpc" in data:
            args["has_grpc"] = data["has_grpc"]
        if "repository_url" in data:
            args["repository_url"] = data["github"]

        return cls(**args)


class Config:
    catalog_endpoint: str

    def __init__(self, catalog_endpoint: str = ""):
        self.catalog_endpoint = catalog_endpoint

    @classmethod
    def from_env(cls) -> typing.Self:
        return cls(
            catalog_endpoint=os.environ.get(
                "CATALOG_ENDPOINT", "http://localhost:8082/api/services"
            )
        )


class Client:
    config: Config

    def __init__(self, config: Config):
        self.config = config

    def services(self) -> typing.List[Service]:
        response = requests.get(self.config.catalog_endpoint)
        if response.status_code != 200:
            raise RuntimeError(
                f"could not fetch service catalog: expected 200, got {response.status_code}"
            )

        return [Service.from_json(item) for item in response.json()]

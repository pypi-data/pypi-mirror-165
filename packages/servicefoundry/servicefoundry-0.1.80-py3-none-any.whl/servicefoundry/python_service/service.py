import json
import sys
from typing import Callable, Dict, List, Optional

import yaml
from pydantic import BaseModel

from servicefoundry.auto_gen.models import Port, Resources
from servicefoundry.python_service.app import build_and_run_app_in_background_thread
from servicefoundry.python_service.remote import RemoteClass
from servicefoundry.python_service.route import RouteGroups
from servicefoundry.v2.lib import Build, LocalSource, PythonBuild, Service
from servicefoundry.version import __version__


class BuildConfig(BaseModel):
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}"
    pip_packages: Optional[List[str]]
    requirements_path: Optional[str] = None

    def __init__(self, **data):
        pip_packages = data.get("pip_packages", [])
        # locally version == 0.0.0
        # pip_packages.append(f"servicefoundry=={__version__}")
        pip_packages.append("servicefoundry[service]>=0.1.77")
        data["pip_packages"] = pip_packages
        super().__init__(**data)

    def to_tfy_python_build_config(
        self, port: int, route_groups: RouteGroups
    ) -> PythonBuild:
        escaped_route_groups_json = json.dumps(route_groups.json())
        return PythonBuild(
            python_version=self.python_version,
            pip_packages=self.pip_packages,
            requirements_path=self.requirements_path,
            command=f"python -m servicefoundry.python_service run --port {port} --route-groups-json {escaped_route_groups_json}",
            # command=f'sleep 300',
        )


class PythonService:
    def __init__(
        self,
        name: str,
        ###
        # Maybe be this should be present in the `deploy` function.
        #
        build_config: Optional[BuildConfig] = None,
        resources: Optional[Resources] = None,
        replicas: int = 1,
        port: int = 8000
        ###
    ):
        self._name = name
        self._build_config = build_config or BuildConfig()
        self._resources = resources or Resources()
        self._replicas = replicas
        self._port = port

        self._route_groups: RouteGroups = RouteGroups()

    @property
    def route_groups(self) -> RouteGroups:
        return self._route_groups

    def __repr__(self):
        return yaml.dump(
            dict(
                name=self._name,
                build_config=self._build_config.dict(),
                resources=self._resources.dict(),
                routes=self._route_groups.dict(),
                replicas=self._replicas,
                port=self._port,
            ),
            indent=2,
        )

    def register_function(
        self,
        func: Callable,
        path: Optional[str] = None,
    ):
        self._route_groups.register_function(func=func, path=path)

    def register_class(self, remote_class: RemoteClass):
        self._route_groups.register_class(remote_class=remote_class)

    def run(self) -> "threading.Thread":
        return build_and_run_app_in_background_thread(
            route_groups=self._route_groups, port=self._port
        )

    def get_deployment_definition(self, workspace_fqn: str, **kwargs) -> Service:
        # Keeping this function right now so that later,
        # the constructor of the application call this function
        # to get the component spec, if an object of this class
        # is directly passed as an component
        tfy_python_build_config = self._build_config.to_tfy_python_build_config(
            port=self._port, route_groups=self._route_groups
        )
        service = Service(
            name=self._name,
            image=Build(build_source=LocalSource(), build_spec=tfy_python_build_config),
            resources=self._resources,
            replicas=self._replicas,
            ports=[Port(port=self._port, expose=True)],
        )
        return service

    def deploy(self, workspace_fqn: str) -> Dict:
        service = self.get_deployment_definition(workspace_fqn=workspace_fqn)
        response = service.deploy(workspace_fqn=workspace_fqn)
        print(response)
        return response

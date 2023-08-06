import yaml
from pydantic import Field, constr

from servicefoundry.auto_gen import models
from servicefoundry.v2.lib.deploy import (
    Deployment,
    deploy_application,
    deploy_component,
)


class Notebook(models.Notebook):
    type: constr(regex=r"notebook") = "notebook"


class Application(models.Application):
    def deploy(self, workspace_fqn: str, tail_build_logs: bool = False) -> Deployment:
        return deploy_application(
            application=self,
            workspace_fqn=workspace_fqn,
            tail_build_logs=tail_build_logs,
        )

    def yaml(self) -> str:
        return yaml.dump(self.dict(exclude_none=True), indent=2)


class Service(models.Service):
    type: constr(regex=r"service") = "service"
    resources: models.Resources = Field(default_factory=models.Resources)

    def deploy(self, workspace_fqn: str, tail_build_logs: bool = False) -> Deployment:
        return deploy_component(
            component=self, workspace_fqn=workspace_fqn, tail_build_logs=tail_build_logs
        )


class Job(models.Job):
    type: constr(regex=r"job") = "job"
    resources: models.Resources = Field(default_factory=models.Resources)

    def deploy(self, workspace_fqn: str, tail_build_logs: bool = False) -> Deployment:
        return deploy_component(
            component=self, workspace_fqn=workspace_fqn, tail_build_logs=tail_build_logs
        )


class Notebook(models.Notebook):
    type: constr(regex=r"notebook") = "notebook"
    resources: models.Resources = Field(default_factory=models.Resources)

    def deploy(self, workspace_fqn: str) -> Deployment:
        return deploy_component(component=self, workspace_fqn=workspace_fqn)

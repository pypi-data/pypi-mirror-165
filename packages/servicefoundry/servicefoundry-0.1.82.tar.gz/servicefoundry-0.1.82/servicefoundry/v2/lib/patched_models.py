from typing import Union

from pydantic import Field, constr

from servicefoundry.auto_gen import models


class DockerFileBuild(models.DockerFileBuild):
    type: constr(regex=r"dockerfile") = "dockerfile"


class PythonBuild(models.PythonBuild):
    type: constr(regex=r"tfy-python-buildpack") = "tfy-python-buildpack"


class RemoteSource(models.RemoteSource):
    type: constr(regex=r"remote") = "remote"


class LocalSource(models.LocalSource):
    type: constr(regex=r"local") = "local"


class Build(models.Build):
    type: constr(regex=r"build") = "build"
    build_source: Union[
        models.RemoteSource, models.GithubSource, models.LocalSource
    ] = Field(default_factory=LocalSource)


class ManualTrigger(models.ManualTrigger):
    type: constr(regex=r"manual") = "manual"


class ScheduledTrigger(models.ScheduledTrigger):
    type: constr(regex=r"scheduled") = "scheduled"


class GithubSource(models.GithubSource):
    type: constr(regex=r"github") = "github"


class HttpProbe(models.HttpProbe):
    type: constr(regex=r"http") = "http"

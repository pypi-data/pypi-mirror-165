from pydantic import constr

from servicefoundry.auto_gen import models


class Build(models.Build):
    type: constr(regex=r"build") = "build"


class DockerFileBuild(models.DockerFileBuild):
    type: constr(regex=r"dockerfile") = "dockerfile"


class TfyPythonBuild(models.TfyPythonBuild):
    type: constr(regex=r"tfy-python-buildpack") = "tfy-python-buildpack"


class RemoteSource(models.RemoteSource):
    type: constr(regex=r"remote") = "remote"


class LocalSource(models.LocalSource):
    type: constr(regex=r"local") = "local"


class ManualTrigger(models.ManualTrigger):
    type: constr(regex=r"manual") = "manual"


class ScheduledTrigger(models.ScheduledTrigger):
    type: constr(regex=r"scheduled") = "scheduled"


class GithubSource(models.GithubSource):
    type: constr(regex=r"github") = "github"


class HttpProbe(models.HttpProbe):
    type: constr(regex=r"http") = "http"

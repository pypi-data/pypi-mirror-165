from typing import List, TypeVar

from pydantic import BaseModel

from servicefoundry.auto_gen import models as auto_gen_models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.dao.workspace import get_workspace
from servicefoundry.logger import logger
from servicefoundry.v2.lib.models import BuildResponse, Deployment
from servicefoundry.v2.lib.source import local_source_to_remote_source

Component = TypeVar("Component", bound=BaseModel)


def _upload_component_source_if_local(
    component: Component, workspace_fqn: str
) -> Component:
    if (
        hasattr(component, "image")
        and isinstance(component.image, auto_gen_models.Build)
        and isinstance(component.image.build_source, auto_gen_models.LocalSource)
    ):
        new_component = component.copy(deep=True)

        logger.info("Uploading code for %s '%s'", component.type, component.name)

        new_component.image.build_source = local_source_to_remote_source(
            local_source=component.image.build_source,
            workspace_fqn=workspace_fqn,
            component_name=component.name,
        )

        logger.debug("Uploaded code for %s '%s'", component.type, component.name)
        return new_component
    return component


def _tail_build_logs(build_responses: List[BuildResponse]):
    client = ServiceFoundryServiceClient.get_client()

    # TODO: Explore other options like,
    # https://rich.readthedocs.io/en/stable/live.html#live-display
    # How does docker/compose does multiple build logs?
    for build_response in build_responses:
        logger.info("Tailing build logs for '%s'", build_response.componentName)
        client.tail_build_logs(build_response=build_response, wait=True)


def deploy_application(
    application: auto_gen_models.Application,
    workspace_fqn: str,
    tail_build_logs: bool = False,
) -> Deployment:
    logger.info("Deploying application '%s' to '%s'", application.name, workspace_fqn)

    # print(application.yaml())
    workspace_id = get_workspace(workspace_fqn).id
    updated_component_definitions = []

    for component in application.components:
        updated_component = _upload_component_source_if_local(
            component=component, workspace_fqn=workspace_fqn
        )
        updated_component_definitions.append(updated_component)

    new_application_definition = auto_gen_models.Application(
        name=application.name, components=updated_component_definitions
    )
    client = ServiceFoundryServiceClient.get_client()
    response = client.deploy_application(
        workspace_id=workspace_id, application=new_application_definition
    )
    logger.info(
        "Application '%s' deployed. Current version is '%s'",
        application.name,
        response.version,
    )
    # TODO: look at build and deploy status
    # If there was any error, put error messages accordingly
    if tail_build_logs:
        _tail_build_logs(build_responses=response.builds)
    return response


def deploy_component(
    component: Component, workspace_fqn: str, tail_build_logs: bool = False
) -> Deployment:
    application = auto_gen_models.Application(
        name=component.name, components=[component]
    )
    return deploy_application(
        application=application,
        workspace_fqn=workspace_fqn,
        tail_build_logs=tail_build_logs,
    )

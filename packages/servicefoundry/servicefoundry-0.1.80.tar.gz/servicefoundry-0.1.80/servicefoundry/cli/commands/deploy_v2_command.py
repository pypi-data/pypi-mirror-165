import rich_click as click
import yaml

from servicefoundry.cli.const import GROUP_CLS
from servicefoundry.cli.display_util import print_json


@click.group(
    name="deploy",
    cls=GROUP_CLS,
    invoke_without_command=True,
    help="Deploy servicefoundry Service",
)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default="./servicefoundry.yaml",
    help="path to servicefoundry file",
)
@click.option(
    "-w",
    "--workspace-fqn",
    type=click.STRING,
    default=None,
    help="workspace to deploy to",
)
def deploy_v2_command(file: str, workspace_fqn: str):
    from servicefoundry.v2 import Application

    with open(file, "r") as f:
        application_definition = yaml.safe_load(f)

    application = Application.parse_obj(application_definition)
    deployment = application.deploy(workspace_fqn=workspace_fqn, tail_build_logs=True)
    # print_json(deployment)

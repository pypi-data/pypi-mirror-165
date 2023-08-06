import os
import tempfile

from servicefoundry.auto_gen import models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.utils.file_utils import make_tarfile
from servicefoundry.v2.lib.patched_models import RemoteSource


def local_source_to_remote_source(
    local_source: models.LocalSource,
    workspace_fqn: str,
    component_name: str,
) -> RemoteSource:
    with tempfile.TemporaryDirectory() as local_dir:
        package_local_path = os.path.join(local_dir, "build.tar.gz")
        make_tarfile(
            output_filename=package_local_path,
            source_dir=local_source.project_root_path,
            additional_directories=[],
            ignore_list=[local_dir],
        )
        client = ServiceFoundryServiceClient.get_client()
        presigned_url = client.upload_code_package(
            workspace_fqn=workspace_fqn,
            component_name=component_name,
            package_local_path=package_local_path,
        )
        return RemoteSource(remote_uri=presigned_url.presigned_url)

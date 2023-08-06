import logging

from servicefoundry import Build, LocalSource, PythonBuild, Resources, Service

logging.basicConfig(level=logging.INFO)
service = Service(
    # name="my-service",
    name="my-service-1",
    image=Build(
        build_spec=PythonBuild(
            command="uvicorn main:app --port 4000 --host 0.0.0.0",
            pip_packages=[
                "fastapi",
                "uvicorn",
            ],
            python_version="3.9",
        ),
    ),
    ports=[{"expose": True, "port": 4000}],
    replicas=2,
    resources=Resources(cpu_limit="600m"),
)
deployment = service.deploy(workspace_fqn="v1:local:my-ws-2")

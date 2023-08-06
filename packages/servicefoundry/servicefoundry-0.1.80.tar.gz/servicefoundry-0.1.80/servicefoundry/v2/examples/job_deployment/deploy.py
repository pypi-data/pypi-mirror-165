import logging

from servicefoundry import (
    Application,
    Build,
    Job,
    LocalSource,
    ManualTrigger,
    PythonBuild,
    ScheduledTrigger,
)

logging.basicConfig(level=logging.INFO)

job = Job(
    name="my-job-manual",
    image=Build(
        build_spec=PythonBuild(command="python main.py --upto 30"),
    ),
)
job.deploy(workspace_fqn="v1:local:my-ws-2")


job = Job(
    name="my-job-scheduled",
    image=Build(
        build_spec=PythonBuild(command="python main.py --upto 30"),
    ),
    trigger=ScheduledTrigger(schedule="*/1 * * * *"),
)
job.deploy(workspace_fqn="v1:local:my-ws-2")

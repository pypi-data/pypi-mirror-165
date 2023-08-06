from my_module import normal, uniform

from servicefoundry import Resources
from servicefoundry.python_service import BuildConfig, PythonService

random_service = PythonService(
    name="random-service",
    build_config=BuildConfig(pip_packages=["numpy<1.22.0"]),
    resources=Resources(cpu_limit="500m", memory_limit="512Mi"),
    replicas=2,
    port=4000,
)
random_service.register_function(normal)
random_service.register_function(uniform)

print(random_service)
random_service.deploy("v1:local:my-ws-2")
# random_service.run().join()

from my_module import Model, preprocess

from servicefoundry.python_service import PythonService, remote

preprocess_service = PythonService("preprocess", port=4000)
preprocess_service.register_function(preprocess)

model_service = PythonService("model-service", port=4001)
model_service.register_class(remote(Model, init_kwargs={"path": "foo"}, name="model"))

preprocess_service.run()
model_service.run().join()

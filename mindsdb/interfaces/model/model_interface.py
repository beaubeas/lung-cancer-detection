import time
import pickle
import os

from mindsdb.utilities.log import log
import pyarrow.flight as fl


class ModelInterfaceWrapper(object):
    def __init__(self, model_interface, company_id=None):
        self.company_id = company_id
        self.model_interface = model_interface

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if kwargs.get('company_id') is None:
                kwargs['company_id'] = self.company_id
            return getattr(self.model_interface, name)(*args, **kwargs)
        return wrapper


class ModelInterfaceNativeImport():
    def __init__(self):
        from mindsdb.interfaces.model.model_controller import ModelController
        self.controller = ModelController(False)

    def create(self, *args, **kwargs):
        return self.controller.create(*args, **kwargs)

    def learn(self, *args, **kwargs):
        return self.controller.learn(*args, **kwargs)

    def predict(self, *args, **kwargs):
        return self.controller.predict(*args, **kwargs)

    def analyse_dataset(self, *args, **kwargs):
        return self.controller.analyse_dataset(*args, **kwargs)

    def get_model_data(self, *args, **kwargs):
        return self.controller.get_model_data(*args, **kwargs)

    def get_models(self, *args, **kwargs):
        return self.controller.get_models(*args, **kwargs)

    def delete_model(self, *args, **kwargs):
        return self.controller.delete_model(*args, **kwargs)

    def update_model(self, *args, **kwargs):
        return 'Model updating is no available in this version of mindsdb'

try:
    from mindsdb_worker.cluster.ray_interface import ModelInterfaceRay
    import ray
    try:
        ray.init(ignore_reinit_error=True, address='auto')
    except Exception:
        ray.init(ignore_reinit_error=True)
    ModelInterface = ModelInterfaceRay
    ray_based = True
except Exception as e:
    ModelInterface = ModelInterfaceNativeImport
    ray_based = False

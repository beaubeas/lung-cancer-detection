# @TODO, replace with arrow later: https://mirai-solutions.ch/news/2020/06/11/apache-arrow-flight-tutorial/
import xmlrpc
import xmlrpc.client
import time
import pickle

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


class ServerProxy(object):
    def __init__(self):
        self._xmlrpc_server_proxy = xmlrpc.client.ServerProxy("http://localhost:19329/", allow_none=True)

    def __getattr__(self, name):
        call_proxy = getattr(self._xmlrpc_server_proxy, name)

        def _call(*args, **kwargs):
            return call_proxy(args, kwargs)
        return _call


class ModelInterfaceRPC():
    def __init__(self):
        for _ in range(10):
            try:
                time.sleep(3)
                self.client = fl.connect("grpc://localhost:19329")
                res = self._action('ping')
                assert self._loads(res)
                return
            except Exception:
                import traceback
                print(traceback.format_exc())
                log.info('Wating for native RPC server to start')
        raise Exception('Unable to connect to RPC server')

    def _action(self, act_name, *args, **kwargs):
        action = fl.Action(act_name, pickle.dumps({'args': args, 'kwargs': kwargs}))
        return self.client.do_action(action)

    def _loads(self, res):
        return pickle.loads(next(iter(res)).body.to_pybytes())

    def create(self, *args, **kwargs):
        self._action('create', *args, **kwargs)

    def learn(self, *args, **kwargs):
        self._action('learn', *args, **kwargs)

    def predict(self, *args, **kwargs):
        res = self._action('predict', *args, **kwargs)
        return self._loads(res)

    def analyse_dataset(self, *args, **kwargs):
        res = self._action('analyse_dataset', *args, **kwargs)
        return self._loads(res)

    def get_model_data(self, *args, **kwargs):
        res = self._action('get_model_data', *args, **kwargs)
        return self._loads(res)

    def get_models(self, *args, **kwargs):
        res = self._action('get_models', *args, **kwargs)
        return self._loads(res)

    def delete_model(self, *args, **kwargs):
        self._action('delete_model', *args, **kwargs)

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
except Exception:
    ModelInterface = ModelInterfaceRPC
    ray_based = False

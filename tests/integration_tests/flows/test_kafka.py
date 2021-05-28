import time
import tempfile
import unittest
import json
import uuid
import threading

import requests
import kafka
import pandas as pd

from common import HTTP_API_ROOT, run_environment, EXTERNAL_DB_CREDENTIALS, USE_EXTERNAL_DB_SERVER


INTEGRATION_NAME = 'test_kafka'
kafka_creds = {}
if USE_EXTERNAL_DB_SERVER:
    with open(EXTERNAL_DB_CREDENTIALS, 'rt') as f:
        kafka_creds = json.loads(f.read())['kafka']


KAFKA_PORT = kafka_creds.get('port', 9092)
KAFKA_HOST = kafka_creds.get('host', "127.0.0.1")

CONNECTION_PARAMS = {"bootstrap_servers": [f"{KAFKA_HOST}:{KAFKA_PORT}"]}
STREAM_SUFFIX = uuid.uuid4()
STREAM_IN = f"test_stream_in_{STREAM_SUFFIX}"
STREAM_OUT = f"test_stream_out_{STREAM_SUFFIX}"
STREAM_IN_TS = f"test_stream_in_ts_{STREAM_SUFFIX}"
STREAM_OUT_TS = f"test_stream_out_ts_{STREAM_SUFFIX}"
DS_NAME = "kafka_test_ds"

def read_stream(stream_name, buf, stop_event):
    consumer = kafka.KafkaConsumer(**CONNECTION_PARAMS, consumer_timeout_ms=1000)
    consumer.subscribe([stream_name])
    while not stop_event.wait(0.5):
        try:
            msg = next(consumer)
            buf.append(json.loads(msg.value))
        except StopIteration:
            pass
    consumer.close()
    print(f"STOPPING READING STREAM {stream_name} THREAD PROPERLY")

class KafkaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        run_environment(apis=['mysql', 'http'])

    def upload_ds(self, name):
        df = pd.DataFrame({
                'group': ["A" for _ in range(100, 210)],
                'order': [x for x in range(100, 210)],
                'x1': [x for x in range(100,210)],
                'x2': [x*2 for x in range(100,210)],
                'y': [x*3 for x in range(100,210)]
            })
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False) as f:
            df.to_csv(f, index=False)
            f.flush()
            url = f'{HTTP_API_ROOT}/datasources/{name}'
            data = {"source_type": (None, 'file'),
                    "file": (f.name, f, 'text/csv'),
                    "source": (None, f.name.split('/')[-1]),
                    "name": (None, name)}
            res = requests.put(url, files=data)
            res.raise_for_status()

    def train_predictor(self, ds_name, predictor_name):
        params = {
            'data_source_name': ds_name,
            'to_predict': 'y',
            'kwargs': {
                'stop_training_in_x_seconds': 20,
                'join_learn_process': True
            }
        }
        url = f'{HTTP_API_ROOT}/predictors/{predictor_name}'
        res = requests.put(url, json=params)
        res.raise_for_status()

    def train_ts_predictor(self, ds_name, predictor_name):
        params = {
            'data_source_name': ds_name,
            'to_predict': 'y',
            'kwargs': {
                'use_gpu': False,
                'join_learn_process': True,
                'ignore_columns': None,
                'timeseries_settings': {"order_by": ["order"],
                                        "group_by": ["group"],
                                        "nr_predictions": 1,
                                        "use_previous_target": True,
                                        "window": 10},
            }
        }
        url = f'{HTTP_API_ROOT}/predictors/{predictor_name}'
        res = requests.put(url, json=params)
        res.raise_for_status()

    def test_1_create_integration(self):
        print(f'\nExecuting {self._testMethodName}')
        url = f'{HTTP_API_ROOT}/config/integrations/{INTEGRATION_NAME}'
        params = {"type": "kafka",
                  "connection": CONNECTION_PARAMS,
                 }
        try:
            res = requests.put(url, json={"params": params})
            self.assertTrue(res.status_code == 200, res.text)
        except Exception as e:
            self.fail(e)


    def test_2_create_kafka_stream(self):
        print(f'\nExecuting {self._testMethodName}')
        try:
            self.upload_ds(DS_NAME)
        except Exception as e:
            self.fail(f"couldn't upload datasource: {e}")

        try:
            self.train_predictor(DS_NAME, self._testMethodName)
        except Exception as e:
            self.fail(f"couldn't train predictor: {e}")

        params = {"predictor": self._testMethodName,
                  "stream_in": STREAM_IN,
                  "stream_out": STREAM_OUT,
                  "integration_name": INTEGRATION_NAME}

        try:
            url = f'{HTTP_API_ROOT}/streams/{self._testMethodName}_{STREAM_SUFFIX}'
            res = requests.put(url, json={"params": params})
            self.assertTrue(res.status_code == 200, res.text)
        except Exception as e:
            self.fail(f"error creating stream: {e}")

    def test_3_making_stream_prediction(self):
        print(f'\nExecuting {self._testMethodName}')
        producer = kafka.KafkaProducer(**CONNECTION_PARAMS)

        # wait when the integration launch created stream
        time.sleep(10)
        predictions = []
        stop_event = threading.Event()
        reading_th = threading.Thread(target=read_stream, args=(STREAM_OUT, predictions, stop_event))
        reading_th.start()
        time.sleep(1)

        for x in range(1, 3):
            when_data = {'x1': x, 'x2': 2*x}
            to_send = json.dumps(when_data)
            producer.send(STREAM_IN, to_send.encode("utf-8"))
        producer.close()
        threshold = time.time() + 120
        while len(predictions) != 2 and time.time() < threshold:
            time.sleep(1)
        stop_event.set()
        self.assertTrue(len(predictions)==2, f"expected 2 predictions but got {len(predictions)}")

    def test_4_create_kafka_ts_stream(self):
        print(f'\nExecuting {self._testMethodName}')
        try:
            self.train_ts_predictor(DS_NAME, self._testMethodName)
        except Exception as e:
            self.fail(f"couldn't train ts predictor: {e}")

        params = {"predictor": self._testMethodName,
                  "stream_in": STREAM_IN_TS,
                  "stream_out": STREAM_OUT_TS,
                  "integration_name": INTEGRATION_NAME,
                  "type": "timeseries"}

        try:
            url = f'{HTTP_API_ROOT}/streams/{self._testMethodName}_{STREAM_SUFFIX}'
            res = requests.put(url, json={"params": params})
            self.assertTrue(res.status_code == 200, res.text)
        except Exception as e:
            self.fail(f"error creating stream: {e}")

    def test_5_making_ts_stream_prediction(self):
        print(f'\nExecuting {self._testMethodName}')
        producer = kafka.KafkaProducer(**CONNECTION_PARAMS)

        # wait when the integration launch created stream
        time.sleep(15)
        predictions = []
        stop_event = threading.Event()
        reading_th = threading.Thread(target=read_stream, args=(STREAM_OUT_TS, predictions, stop_event))
        reading_th.start()
        time.sleep(3)

        for x in range(210, 221):
            when_data = {'x1': x, 'x2': 2*x, 'order': x, 'group': "A"}
            to_send = json.dumps(when_data)
            producer.send(STREAM_IN_TS, to_send.encode("utf-8"))
        producer.close()

        threshold = time.time() + 120
        while len(predictions) != 2 and time.time() < threshold:
            time.sleep(1)
        stop_event.set()
        self.assertTrue(len(predictions)==2, f"expected 2 predictions, but got {len(predictions)}")

if __name__ == "__main__":
    try:
        unittest.main(failfast=True)
        print('Tests passed!')
    except Exception as e:
        print(f'Tests Failed!\n{e}')

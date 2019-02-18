

DEFAULT_ORDER_BY_TYPE = 'DESC'
TRANSACTION_LEARN = 'learn'
TRANSACTION_PREDICT = 'predict'
TRANSACTION_LOAD = 'load'
TRANSACTION_CLUSTER = 'cluster'
TRANSACTION_NORMAL_SELECT = 'normal_select'
TRANSACTION_NORMAL_MODIFY = 'normal_modify'
TRANSACTION_BAD_QUERY = 'bad_query'
TRANSACTION_SHOW_DATASOURCES = 'show_datasources'
TRANSACTION_DROP_MODEL ='drop_model'

STOP_TRAINING = 'stop_training'
KILL_TRAINING = 'kill_training'

KEY_COLUMNS = 'columns'
KEY_STATS = 'stats'
KEY_MODEL_METADATA = 'model_metadata'
KEY_MODEL_NAME = 'model_name'
KEY_SUBMODEL_NAME = 'submodel_name'
KEY_MODEL_QUERY = 'model_query'
KEY_MODEL_TEST_QUERY = 'model_test_query'
KEY_MODEL_GROUP_BY = 'model_group_by'
KEY_MODEL_ORDER_BY = 'model_order_by'
KEY_MODEL_PREDICT_COLUMNS = 'model_predict_columns'
KEY_MODEL_WHEN_CONDITIONS = 'model_when_conditions'
KEY_MODEL_UPDATE_FREQUENCY = 'model_upate_frequency'
KEY_MODEL_CACHE_RESULTS = 'model_cache_results'
KEY_MODEL_CACHE = 'model_cache'
KEY_COLUMN_MAP = 'column_map'
KEY_MODEL_MODEL_TYPE = 'predictor'
KEY_MODEL_PREDICT_FROM_TABLE = 'model_predict_from_table'
KEY_CONFIDENCE ='prediction_confidence'

KEY_TRANSACTION_TYPE = 'transaction_type'

LEARNING_RATE_INDEX = 0
EPOCHS_INDEX = 1

KEY_NO_GROUP_BY = 'ALL_ROWS_NO_GROUP_BY'

KEY_START = 'start'
KEY_END = 'end'
KEY_METADATA = 'metadata'
KEY_STATUS = 'status'

FULL_TEXT_ENCODING_EXTRA_LENGTH = 4 #(len)[is_start, is_end, unfrequent_word, is_null]
FULL_TEXT_NONE_VALUE = 0
FULL_TEXT_IS_START = 1
FULL_TEXT_IS_END = 2
FULL_TEXT_UN_FREQUENT = 3

EXTENSION_COLUMNS_TEMPLATE = '_extensions_.buckets.{column_name}'

TEXT_ENCODING_EXTRA_LENGTH = 2 #(len)[unfrequent_word, is_null]

ALL_INDEXES_LIST = ['*']

class DATA_TYPES:
    NUMERIC = 'Numeric'
    DATE = 'Date'
    TEXT = 'Text'
    CATEGORICAL = 'Class'

class SAMPLE_TYPES:
    TEST_SET = 'test'
    TRAIN_SET = 'train'
    PREDICT_SET = 'predict'

class SAMPLER_MODES:
    LEARN = 'learn'
    PREDICT = 'predict'
    DEFAULT = None

class KEYS:
    TEST_SET = 'test'
    TRAIN_SET = 'train'
    PREDICT_SET = 'predict'

    ALL_SET = 'all'
    X ='x'
    Y ='y'
    DATA_TYPE = 'DataType'
    TS_ENCODED_ROW = 'TS_ENCODED_ROW'
    TS_FLAT_ROW = 'TS_FLAT_ROW'

class ORDER_BY_KEYS:
    COLUMN = 0
    ASCENDING_VALUE = 1

class PREDICTORS:
    DEFAULT = 'default'
    CUSTOM = 'custom'

class FRAMEWORKS:
    PYTORCH = 'pytorch'
    TENSORFLOW = 'tensorflow'
    KERAS = 'keras'


PHASE_START = 0
PHASE_END = 1000
PHASE_DATA_EXTRACTOR = 1
PHASE_STATS_GENERATOR = 2
PHASE_DATA_VECTORIZER = 3
PHASE_DATA_ENCODER = 4
PHASE_MODEL_TRAINER = 5
PHASE_PREDICTION = 5
PHASE_DATA_DEVECTORIZATION = 6
PHASE_MODEL_ANALYZER = 7

MODEL_STATUS_TRAINED = "Trained"
MODEL_STATUS_PREPARING = "Preparing"
MODEL_STATUS_TRAINING= "Training"
MODEL_STATUS_ANALYZING = "Analyzing"
MODEL_STATUS_ERROR = "Error"

WORD_SEPARATORS = [',', "\t", ' ']
NULL_VALUES = [None, '']

SAMPLER_FLAT_TENSORS = 'flat_vectors'
SAMPLER_COLUMN_TENSORS = 'column_tensors'

MODEL_GROUP_BY_DEAFAULT_LIMIT = 80

DEBUG_LOG_LEVEL = 10
INFO_LOG_LEVEL = 20
WARNING_LOG_LEVEL = 30
ERROR_LOG_LEVEL = 40
NO_LOGS_LOG_LEVEL = 50

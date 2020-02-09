
import json
from .common import *


class Encoder:
    @staticmethod
    def load_expiration_synch_msg(key):
        expiration_dict = {}
        expiration_dict[COMMAND] = EXPIRATION_COMMAND
        expiration_dict[EXPIRATION_KEY_START] = key
        return json.dumps(expiration_dict)

    @staticmethod
    def load_get_synch_msg(key):
        get_dict = {}
        get_dict[COMMAND] = GET_COMMAND
        get_dict[DICT_KEY] = key
        return json.dumps(get_dict)

    @staticmethod
    def load_reload_msg():
        dict1 = {}
        dict1[COMMAND] = RECOVERY_COMMAND
        return json.dumps(dict1)

    @staticmethod
    def load_synch_msg(key, value, timestamp):
        synch_dict = {}
        synch_dict[COMMAND] = SYNCH_COMMAND
        data = {}
        data_list = []
        data[DICT_KEY] = key
        data[DICT_VALUE] = value
        data[DICT_TIME] = timestamp
        data_list.append(data)
        synch_dict[DATA_FIELD] = data_list
        return json.dumps(synch_dict)
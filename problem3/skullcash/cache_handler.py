'''
Cache Handler Service class object holding all of the data
'''
import websockets
import logging
import time
import json
import asyncio
from .cache_dlinked_list import CacheList
from .sync_cache import SyncCache
from .common import *


class CacheHandler:

    def __init__(self, cache_size, expiration_limit, distributed = False, remote_addresses = None):
        '''
        Class to handle all cache calls, heart of this library
        :param cache_size: Cache Max Size
        :param expiration_limit: Expiration Limit of Cache data
        :param distributed: Distributed is True when accessed from DistributedCache otherwise False
        :param remote_addresses: Address of Remote Cache Instances
        '''
        self.cache_list = CacheList()
        self.cache_dict = {}

        self.cache_size = cache_size
        self.expiration_limit_value = expiration_limit
        self.distributed = distributed
        self.rd = None

        if distributed is True:
            self.sync_cache = SyncCache(remote_addresses, self)
            self.lock = asyncio.Lock()

    async def reload_values(self):
        asyncio.ensure_future(self.sync_cache.reload())

    def set_reload_data(self, rd):
        self.reload_data = rd

    def synch_with_remote(self, dict_list):
        for dict_value in dict_list:
            self.set(dict_value[DICT_KEY], dict_value[DICT_VALUE], dict_value[DICT_TIME], remote = True)

    async def handle(self, websocket, path):
        try:
            async for message in websocket:
                try:
                    message_json = json.loads(message)
                    if COMMAND in message_json:
                        if message_json[COMMAND] == SYNCH_COMMAND:
                            synch_msg_list = message_json[DATA_FIELD]
                            async with self.lock:
                                self.synch_with_remote(synch_msg_list)
                            continue

                        elif message_json[COMMAND] == 'get':
                            self.get(message_json[DICT_KEY], remote = True)

                        elif message_json[COMMAND] == EXPIRATION_COMMAND:
                            expired_key = message_json[EXPIRATION_KEY_START]
                            async with self.lock:
                                self.clear_expired_keys(self.cache_dict[expired_key][DICT_NODE])
                            await websocket.send(json.dumps({COMMAND: EXPIRATION_COMMAND, 'result': True}))
                            continue

                        elif message_json[COMMAND] == RECOVERY_COMMAND:
                            async with self.lock:
                                await self.send_recovery_data_back(websocket)
                            continue
                        else:
                            print("wrong message")

                    else:
                        responseMsg = {}
                        responseMsg[COMMAND] = 'ping'
                        await websocket.send(json.dumps(responseMsg))

                except Exception as e:
                    LOG.error(e)
                    # await self.send_error(websocket)
                    continue
        except Exception:
            LOG.error('client disconnected, removed as subscriber: ' + str(
                websocket.remote_address))

    async def send_recovery_data_back(self, websocket):
        list_iter = self.cache_list.iterate_over_all_nodes()
        recovery_list = []
        for item in list_iter:
            stored_dict = self.cache_dict[item.get_value()]
            recovery_dict = {}
            recovery_dict[DICT_KEY] = item.get_value()
            recovery_dict[DICT_VALUE] = stored_dict[DICT_VALUE]
            recovery_dict[DICT_TIME] = stored_dict[DICT_TIME]
            recovery_list.append(recovery_dict)

        sending_dict = {}
        sending_dict[COMMAND] = RECOVERY_COMMAND
        sending_dict[DATA_FIELD] = recovery_list

        await websocket.send(json.dumps(sending_dict))


    def clear_expired_keys(self, key_node):
        expired_keys = self.cache_list.pop_expired_nodes(key_node)
        print(expired_keys)
        for exp_key in expired_keys:
            del self.cache_dict[exp_key]
            logging.debug('Cache entry removed for key {} due to expiration'.format(exp_key))

    def get(self, key, remote = False):
        ''''
        Get the value associated with key
        '''
        LOG.info('Retrieving value for key {}'.format(key))
        if key in self.cache_dict:
            current_time = time.time()
            dict_value = self.cache_dict.get(key)

            if current_time - dict_value[DICT_TIME] < self.expiration_limit_value:
                self.cache_list.remove_cache_node(dict_value[DICT_NODE])
                node = self.cache_list.add_to_head(key)

                dict_value[DICT_NODE] = node
                dict_value[DICT_TIME] = current_time
                self.cache_dict[key] = dict_value
                if self.distributed is True and remote is False:
                    asyncio.ensure_future(self.sync_cache.get_synch(key))
                return dict_value.get(DICT_VALUE)

            else:
                self.clear_expired_keys(dict_value[DICT_NODE])
                if self.distributed is True and remote is False:
                    self.sync_cache.synch_expiration(key)
                    self.sync_cache.expiration_wait()
                logging.warning("Cache entry for key {} expired".format(key))
                return None
        else:
            logging.info('Cache Miss - no data present for the provided {} key'.format(key))
            return None

    def set(self, key, value, timestamp_value = time.time(), remote = False):
        '''
        Sey the value for key
        '''
        try:
            LOG.info("Storing {} key with value {}".format(key,value))
            if key in self.cache_dict:
                value_dict = self.cache_dict.get(key)
                removable_node = value_dict.get(DICT_NODE)
                self.cache_list.remove_cache_node(removable_node)
            else:
                if self.cache_list.get_len() == self.cache_size:
                    key_popped = self.cache_list.pop_from_tail()
                    del self.cache_dict[key_popped]

            node = self.cache_list.add_to_head(key)
            dictionary_construct = {}
            dictionary_construct[DICT_VALUE] = value
            dictionary_construct[DICT_TIME] = timestamp_value
            dictionary_construct[DICT_NODE] = node
            self.cache_dict[key] = dictionary_construct

            if self.distributed is True and remote is False:
                return self.sync_cache.synchronize(key, value, timestamp_value)
        except Exception as e:
            LOG.debug('Set operation for {} key failed'.format(key))
            return False
        return True
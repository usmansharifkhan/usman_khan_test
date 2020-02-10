'''
DistributedCache class can be used to implement a cache service depending on the configuration supplied
'''
from .cache_handler import CacheHandler
import logging
import websockets
import os
import asyncio

CACHE_SERVER_HOST = os.getenv("CACHE_SERVER_HOST", "127.0.0.1")
CACHE_SERVER_PORT = int(os.getenv("CACHE_SERVER_PORT", "6789"))
CACHE_DISTRIBUTION = os.getenv("CACHE_DISTRIBUTION", False)
MAX_CACHE_SIZE = os.getenv("MAX_CACHE_SIZE", 100)
EXPIRATION_EPOCH_MAX_TIME = int(os.getenv("EXPIRATION_EPOCH_MAX_TIME", 10000000000))
REMOTE_SERVER_ADDRESSES = os.getenv('REMOTE_SERVER_ADDRESSES', 'localhost:6788')


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

class DistributedCache:

    def __init__(self, event_loop = None, cache_size = MAX_CACHE_SIZE, expiration_limit = EXPIRATION_EPOCH_MAX_TIME,
                 server_host = CACHE_SERVER_HOST, server_port = CACHE_SERVER_PORT, remote_addresses = REMOTE_SERVER_ADDRESSES):
        if event_loop == None:
            raise Exception("Event loop is invalid, distributed cache depends on Async event loop")


        self.cache_handler = CacheHandler(cache_size, expiration_limit, distributed = True, remote_addresses = remote_addresses)
        server_args = {
            'ws_handler': self.cache_handler.handle,
            'host': server_host,
            'port': server_port
        }
        ws = websockets.serve(**server_args)
        self.task = asyncio.ensure_future(ws)
        asyncio.ensure_future(self.cache_handler.reload_values())

    def get_ws_server(self):
        return self.task

    def get(self, key):
        '''
        Get the value associated with key
        '''
        return self.cache_handler.get(key)

    def set(self, key, value):
        '''
        Set the value for key
        '''
        self.cache_handler.set(key, value)



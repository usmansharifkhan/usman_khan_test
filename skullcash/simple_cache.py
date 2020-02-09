'''
SimpleCache is a single instance cache library
'''

from .cache_handler import CacheHandler
import logging
import os

MAX_CACHE_SIZE = os.getenv("MAX_CACHE_SIZE", 100)
EXPIRATION_EPOCH_MAX_TIME = int(os.getenv("EXPIRATION_EPOCH_MAX_TIME", 10000000000))

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

class SimpleCache:

    def __init__(self, cache_size = MAX_CACHE_SIZE, expiration_limit = EXPIRATION_EPOCH_MAX_TIME):
        LOG.info('Configuration')
        self.cache_handler = CacheHandler(cache_size, expiration_limit)

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
'''
This file contains all the common variables being used in the Cache library
'''
import logging
import os

LOG = logging.getLogger()

COMMAND = 'command'
SYNCH_COMMAND = 'synchronize'
EXPIRATION_COMMAND = 'expire'
RECOVERY_COMMAND = 'recover'
GET_COMMAND = 'get'

DATA_FIELD = 'data'
DICT_KEY = 'key'
DICT_VALUE = 'value'
DICT_TIME = 'time'
DICT_NODE = 'node'

EXPIRATION_KEY_START = 'from_key'



def configure_logging():
  level = os.getenv('LOG_LEVEL', 'info')
  if level.lower() == 'warn':
    level = logging.WARN
  elif level.lower() == 'info':
    level = logging.INFO
  elif level.lower() == 'debug':
    level = logging.DEBUG
  else:
    level = logging.ERROR
  LOG.setLevel(level)
  output_handler = logging.StreamHandler()
  output_handler.setFormatter(logging.Formatter(
      "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"))
  LOG.addHandler(output_handler)

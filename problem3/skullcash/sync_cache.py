'''
SyncCache is a class handling the distributed feature of cache library
'''
import asyncio
import websockets
from .encoder import *


class SyncCache:

    def __init__(self, remote_server_address, cache_handler):

        self._neighbour_addresses = SyncCache._get_list_of_remote_address(remote_server_address)
        self._neighbours = []
        for neighbour in self._neighbour_addresses:
            asyncio.ensure_future(self._connect_exception(neighbour))
        self._cache_handler = cache_handler

    @staticmethod
    def _get_list_of_remote_address(remote_addresses_str):
        remote_addresses_list = remote_addresses_str.split(',')
        for remote_add in remote_addresses_list:
            if remote_add == '':
                raise Exception('Malformed Remote Address')
            remote_add.replace(' ', '')
        return remote_addresses_list

    async def _connect_exception(self, neighbour):
        try:
            ws_conn = await websockets.connect('ws://' + neighbour)
            self._neighbours.append(ws_conn)
        except Exception as e:
            await asyncio.sleep(10)
            await self._connect_exception(neighbour)

    async def send_expiration_msg(self, msg):
        for neighbour in self._neighbours:
            task = asyncio.ensure_future(neighbour.send(msg))

    async def synch_expiration(self, key):
        msg = Encoder.build_expiration_synch_msg(key)
        await self.send_expiration_msg(msg)


    async def reload(self):
        await asyncio.sleep(2)
        reload_msg = Encoder.build_reload_msg()
        neighbour = None
        if len(self._neighbours) == 0:
            return None
        for n in self._neighbours:
            neighbour = n
            await n.send(reload_msg)
            break
        received_msg = await neighbour.recv()
        self._retrieve_apply_reload_data(received_msg)

    def _retrieve_apply_reload_data(self, received_msg):
        msg_dict = json.loads(received_msg)
        data_list = msg_dict[DATA_FIELD]

        for data in data_list:
            self._cache_handler.set(data[DICT_KEY], data[DICT_VALUE], data[DICT_TIME], remote=True)

    async def send_sync_msg(self, msg):
        for neighbour in self._neighbours:
            asyncio.ensure_future(neighbour.send(msg))

    def synchronize(self, key, value, time):
        msg = Encoder.build_synch_msg(key, value, time)
        asyncio.ensure_future(self.send_sync_msg(msg))

    async def get_synch(self, key):
        msg = Encoder.build_get_synch_msg(key)
        for neighbour in self._neighbours:
            asyncio.ensure_future(neighbour.send(msg))




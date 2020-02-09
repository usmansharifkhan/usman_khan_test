'''
SyncCache is a class handling the distributed feature of cache library
'''
import asyncio
import websockets
from .encoder import *


class SyncCache:

    def __init__(self, remote_server_address, cache_handler):

        self._count = 0
        self._neighbour_addresses = SyncCache._get_list_of_remote_address(remote_server_address)
        self._neighbours = []
        self._expiration_set = set()
        self._sync_set = set()
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
            print("Connection attempted")
            ws_conn = await websockets.connect('ws://' + neighbour)
            print("connection acquired")
            self._neighbours.append(ws_conn)
        except Exception as e:
            print("Connection Failed")
            await asyncio.sleep(10)
            await self._connect_exception(neighbour)


    def expiration_done_callback(self, task):
        self._expiration_set.remove(task)

    async def send_expiration_msg(self, msg):
        for neighbour in self._neighbours:
            task = asyncio.ensure_future(neighbour.send(msg))
            self._expiration_set.add(task)
            task.add_done_callback(self.expiration_done_callback(task))

    async def synch_expiration(self, key):
        msg = Encoder.load_expiration_synch_msg(key)
        await self.send_expiration_msg(msg)

    async def expiration_wait(self):
        if self._expiration_set:
            await asyncio.wait(self._expiration_set)


    async def reload(self):
        await asyncio.sleep(2)
        msg = Encoder.load_reload_msg()
        neighbour = None
        if len(self._neighbours) == 0:
            return None
        for n in self._neighbours:
            neighbour = n
            await n.send(msg)
            break

        received_msg = await neighbour.recv()
        msg_dict = json.loads(received_msg)
        data = msg_dict['data']

        for x in data:
            self._cache_handler.set(x[DICT_KEY], x[DICT_VALUE], x[DICT_TIME], remote = True)




    async def send_sync_msg(self, msg):
        for neighbour in self._neighbours:
            asyncio.ensure_future(neighbour.send(msg))

    def synchronize(self, key, value, time):
        msg = Encoder.load_synch_msg(key, value, time)
        asyncio.ensure_future(self.send_sync_msg(msg))

    def sync_done_callback(self, task):
        self._sync_set.remove(task)

    async def get_synch(self, key):
        msg = Encoder.load_get_synch_msg(key)
        for neighbour in self._neighbours:
            asyncio.ensure_future(neighbour.send(msg))




'''
This python file is just a playground for initial testing
'''
import asyncio

from .skullcash.distributed_cache import DistributedCache


async def set_values():
    for x in range(100):
        cache.set('key'+ str(x), 'value' + str(x))
        cache.get('key' + str(x))
        await asyncio.sleep(2)

async def get_values():
    for x in range(100):
        # cache.set('key'+ str(x), 'value' + str(x))
        print(cache.get('key' + str(x)))
        await asyncio.sleep(2)

if __name__ == '__main__':
    print("Server started")

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    cache = DistributedCache(event_loop, cache_size = 100)

    stop = asyncio.Future()
    asyncio.ensure_future(get_values())
    event_loop.run_until_complete(stop)

    ws_server = cache.get_ws_server()
    ws_server.close()
    event_loop.run_until_complete(ws_server.wait_closed())
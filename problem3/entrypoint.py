
import asyncio
import signal

from .skullcash.distributed_cache import DistributedCache

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    cache = DistributedCache(event_loop)

    stop = asyncio.Future()
    event_loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    event_loop.run_until_complete(stop)

    ws_server = cache.get_ws_server()
    ws_server.close()
    event_loop.run_until_complete(ws_server.wait_closed())
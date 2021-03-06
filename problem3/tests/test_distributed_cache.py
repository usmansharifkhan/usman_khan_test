

from ..skullcash.distributed_cache import DistributedCache
import asyncio
import pytest
import signal


@pytest.mark.asyncio
async def test_distributed_sync(event_loop):
    cache1 = DistributedCache(event_loop, remote_addresses = 'localhost:6788,localhost:6787')
    cache2 = DistributedCache(event_loop, server_port = 6788, remote_addresses = 'localhost:6789,localhost:6787')
    cache3 = DistributedCache(event_loop, server_port = 6787, remote_addresses='localhost:6789,localhost:6788')
    await asyncio.sleep(2)

    for x in range(10):
        cache1.set('key' + str(x), 'value' + str(x))

    await asyncio.sleep(2)
    for x in range(10):
        assert cache1.get('key' + str(x)) == cache2.get('key' + str(x)) == cache3.get('key' + str(x)) == 'value' + str(x)

    for x in range(50):
        cache1.set('alt-key' + str(x), 'value' + str(x))
        cache3.set('diff-key' + str(x), 'value' + str(x))
    await asyncio.sleep(2)

    for x in range(40, 50):
        assert cache2.get('alt-key' + str(x)) == cache3.get('alt-key' + str(x))
        assert cache2.get('diff-key' + str(x)) == cache3.get('diff-key' + str(x))
    print("Assertion performed")

    for sig in (signal.SIGINT, signal.SIGTERM):
        event_loop.add_signal_handler(sig, ask_exit)

    cache1.get_ws_server().cancel()
    cache2.get_ws_server().cancel()
    cache3.get_ws_server().cancel()
    await asyncio.sleep(2)
    event_loop.stop()

def ask_exit():
    for task in asyncio.Task.all_tasks():
        task.cancel()



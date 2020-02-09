

from skullcash.distributed_cache import DistributedCache
import asyncio
import pytest


@pytest.mark.asyncio
async def test_distributed_sync(event_loop):
    cache1 = DistributedCache(event_loop, remote_addresses = 'localhost:6788,localhost:6787')
    cache2 = DistributedCache(event_loop, server_port = 6788, remote_addresses = 'localhost:6789,localhost:6787')
    cache3 = DistributedCache(event_loop, server_port = 6787, remote_addresses='localhost:6789,localhost:6788')
    await asyncio.sleep(2)

    for x in range(10):
        cache1.set('key' + str(x), 'value' + str(x))

    await asyncio.sleep(1)
    for x in range(10):
        assert cache1.get('key' + str(x)) == cache2.get('key' + str(x)) == cache3.get('key' + str(x)) == 'value' + str(x)

    for x in range(50):
        cache1.set('alt-key' + str(x), 'value' + str(x))
        cache3.set('diff-key' + str(x), 'value' + str(x))
        # await asyncio.sleep(1)

    print(cache1.get('alt-key49'))
    for x in range(40, 50):
        assert cache2.get('alt-key' + str(x)) == cache3.get('alt-key' + str(x))
        assert cache2.get('diff-key' + str(x)) == cache3.get('diff-key' + str(x))
        assert cache2.get('key' + str(x)) == cache3.get('key' + str(x)) == None
    print("assertion performed")


@pytest.mark.asyncio
async def test_distributed_sync1(event_loop):
    cache1 = DistributedCache(event_loop, server_port = 7789, remote_addresses = 'localhost:7788,localhost:7787')
    cache2 = DistributedCache(event_loop, server_port = 7788, remote_addresses = 'localhost:7789,localhost:7787')
    cache3 = DistributedCache(event_loop, server_port = 7787, remote_addresses='localhost:7789,localhost:7788')
    await asyncio.sleep(2)

    for x in range(200):
        cache1.set('key' + str(x), 'value' + str(x))



    await asyncio.sleep(1)
    for x in range(10):
        assert cache1.get('key' + str(x)) == cache2.get('key' + str(x)) == cache3.get('key' + str(x))



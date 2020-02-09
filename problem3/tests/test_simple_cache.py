
import time
from ..skullcash.simple_cache import SimpleCache


def test_check_set_get_cache():
    simple_cache = SimpleCache()
    for key_num in range(10):
        simple_cache.set('key' + str(key_num), 'value' + str(key_num))
        assert simple_cache.get('key' + str(key_num)) == 'value' + str(key_num)

def test_check_set_get_cache_lru():
    simple_cache = SimpleCache()
    for key_num in range(200):
        simple_cache.set('key' + str(key_num), 'value' + str(key_num))
    for key_num in range(100):
        assert simple_cache.get('key' + str(key_num)) == None
    for key_num in range(101, 200):
        assert simple_cache.get('key' + str(key_num)) == 'value' + str(key_num)

def test_check_set_get_cache_expiration():
    simple_cache = SimpleCache(expiration_limit=1)
    for key_num in range(100):
        simple_cache.set('key' + str(key_num), 'value' + str(key_num))
    time.sleep(1)
    for key_num in range(100):
        # print(simple_cache.get('key' + str(key_num)))
        assert simple_cache.get('key' + str(key_num)) == None


if __name__ == '__main__':
    test_check_set_get_cache()
    test_check_set_get_cache_lru()
    test_check_set_get_cache_expiration()

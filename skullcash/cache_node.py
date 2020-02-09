'''
Cache Node holding the key as a value
'''

class CacheNode(object):
    __slots__ = ('_prev', '_next', '_value')

    def __init__(self, value=None, prev=None, next=None):
        self._prev = prev
        self._next = next
        self._value = value

        if prev is not None:
            prev._next = self
        if next is not None:
            next._prev = self

    def _iter(self, direction):

        current = self
        while current is not None:
            yield current
            current = direction(current)

    def iternext(self):
        return self._iter(lambda x: x._next)

    def iterprev(self):
        return self._iter(lambda x: x._prev)

    def get_prev(self):
        return self._prev

    def get_next(self):
        return self._next

    def get_value(self):
        return self._value

    def set_prev(self, prev):
        self._prev = prev

    def set_next(self, next):
        self._next = next




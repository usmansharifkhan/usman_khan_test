'''
Doubly Cache Linked List giving LRU feature to the library < Faster insertions(O(1)), Faster deletions (O(1)) >
'''
from .cache_node import CacheNode

class CacheList(object):
    __slots__ = ('_first', '_last', '_size')

    def __init__(self, sequence=None):
        '''
        Doubly Linked list containing the sequence of cache
        '''
        self._first = None
        self._last = None
        self._size = 0

        if sequence is None:
            return

        for value in sequence:
            node = CacheNode(value, self._last, None)

            if self._first is None:
                self._first = node
            self._last = node
            self._size += 1

    def get_len(self):
        return self._size

    def add_to_head(self, value):
        '''
        Add the node to the head of the doubly linked list
        '''
        node = CacheNode(value, None, self._first)
        if self._first is not None:
            self._first.set_prev(node)
        if self._last is None:
            self._last = node
        self._first = node
        self._size += 1
        return node

    def pop_from_tail(self):
        '''
        Remove a node from the tail of the doubly linked list
        '''
        if self._last is None:
            raise ValueError("Popping from an empty list is not allowed")
        last = self._last
        self._last = self._last.get_prev()
        if self._last is not None:
            self._last.set_next(None)
        self._size -= 1
        value = last.get_value()
        del last
        return value

    def pop_from_head(self):
        '''
        Removes a node from the head of the doubly linked list
        '''
        if self._first is None:
            raise ValueError("Popping from an empty list is not allowed")
        first = self._first
        self._first = self._first.get_next()
        if self._first is not None:
            self._first.set_prev(None)
        self._size -= 1
        del first

    def remove_cache_node(self, cache_node):
        '''
        Removes a specific cache node, O(n) = 1
        :param cache_node: cache node to be removed from the doubly linked list
        '''
        if self._last is cache_node:
            self.pop_from_tail()
            return

        if self._first is cache_node:
            self.pop_from_head()
            return


        prev_node = cache_node.get_prev()
        next_node = cache_node.get_next()

        prev_node.set_next(next_node)
        next_node.set_prev(prev_node)
        del cache_node
        self._size -= 1

    def pop_expired_nodes(self, node):
        '''
        Removes series of expired cache nodes
        :param node: The node where list is cut off
        :return: List of expired node keys, so that it could be removed from the dictionary as well
        '''
        expired_keys = []

        self._last = node.get_prev()
        if self._last is not None:
            self._last._next = None
        expired_keys.append(node.get_value())
        self._size -= 1

        next_node = node.get_next()

        while next_node != None:
            expired_keys.append(next_node.get_value())
            next_node = next_node.get_next()
            self._size -= 1

        return expired_keys

    def iterate_over_all_nodes(self):
        '''
        Returns an iterator of all nodes
        '''
        if self._first is not None:
            return self._first.iternext()
        else:
            return iter([])

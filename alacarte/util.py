# encoding: utf-8


__all__ = ['Cache']



class Cache(dict):
    """A least-recently-used (LRU) cache.

    Discards the least recently referenced object when full.

    Based on Python Cookbook contributions from multiple sources:

        * http://code.activestate.com/recipes/521871/
        * http://code.activestate.com/recipes/498110/
        * http://code.activestate.com/recipes/252524/
        * http://code.activestate.com/recipes/498245/

    And Genshi's LRUCache:

        http://genshi.edgewall.org/browser/trunk/genshi/util.py

    Warning: If memory cleanup is diabled this dictionary will leak.

    """

    class CacheElement(object):
        def __init__(self, key, value):
            self.previous = self.next = None
            self.key, self.value = key, value

        def __repr__(self):
            return repr(self.value).replace('object at', 'proxy object at')

    def __init__(self, capacity):
        super(Cache, self).__init__()

        self.head = self.tail = None
        self.capacity = capacity

    def __iter__(self):
        cur = self.head

        while cur:
            yield cur.key
            cur = cur.next

    def __getitem__(self, key):
        element = super(Cache, self).__getitem__(key)
        self._update(element)
        return element.value

    def __setitem__(self, key, value):
        try:
            element = super(Cache, self).__getitem__(key)
            element.value = value
            self._update(element)

        except KeyError:
            # Item doesn't exist, create a new wrapper element.
            element = self.CacheElement(key, value)
            super(Cache, self).__setitem__(key, element)
            self._insert(element)

        self._restrict()

    def _insert(self, element):
        element.previous, element.next = None, self.head

        if self.head is not None:
            self.head.previous = element

        else:
            self.tail = element

        self.head = element

    def _restrict(self):
        while len(self) > self.capacity:
            # element = super(Cache, self).get(self.tail.key)
            del self[self.tail.key]

            if self.tail != self.head:
                self.tail = self.tail.previous
                self.tail.next = None

            else:
                self.head = self.tail = None

    def _update(self, element):
        if self.head == element:
            return

        previous = element.previous
        previous.next = element.next

        if element.next is not None:
            element.next.previous = previous

        else:
            self.tail = previous

        element.previous, element.next = None, self.head
        self.head.previous = self.head = element

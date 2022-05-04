#!/usr/bin/env python3
"""FIFO Caching"""

from collections import OrderedDict

baseCaching = __import__("base_caching").BaseCaching


class FIFOCache(baseCaching):
    """inherits from BaseCaching"""

    def __init__(self):
        """initialize"""
        super().__init__()
        # preserve the order in which keys are inserted
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

        if len(self.cache_data.values()) > baseCaching.MAX_ITEMS:
            """discard the first item put in cache (FIFO)"""
            first_key, first_item = self.cache_data.popitem(False)
            print("DISCARD: {}".format(first_key))

    def get(self, key):
        """returns value in self.cache_Data linked to key"""
        return self.cache_data.get(key, None)

#!/usr/bin/env python3
"""LIFO Caching"""

from collections import OrderedDict

baseCaching = __import__("base_caching").BaseCaching


class LIFOCache(baseCaching):
    """inherits from BaseCaching"""

    def __init__(self):
        """initialize"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data.values()) > baseCaching.MAX_ITEMS:
                """discard the first item put in cache (LIFO)"""
                last_key, last_item = self.cache_data.popitem(True)
                print("DISCARD: {}".format(last_key))
        # add a new key with item
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """returns value in self.cache_Data linked to key"""
        return self.cache_data.get(key, None)

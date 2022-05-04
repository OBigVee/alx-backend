#!/usr/bin/env python3
"""LRU Caching"""

from collections import OrderedDict

baseCaching = __import__("base_caching").BaseCaching


class LRUCache(baseCaching):
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
            if len(self.cache_data.values()) + 1 > baseCaching.MAX_ITEMS:
                # print(f"len = {len(self.cache_data.values()) + 1}")
                # print(f"MAX: {baseCaching.MAX_ITEMS}")
                """discard the least recent use item put in cache (LRU algo)"""
                least_recent_use_key, _ = self.cache_data.popitem(True)
                print("DISCARD: {}".format(least_recent_use_key))
            # add a new key with item
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            # add a new key with item
            self.cache_data[key] = item

    def get(self, key):
        """returns value in self.cache_Data linked to key"""
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)

#!/usr/bin/env python3
"""Basic Dict"""

baseCaching = __import__("base_caching").BaseCaching


class BasicCache(baseCaching):
    """inherits from BaseCaching"""
    def __init__(self):
        """initialize"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        try:
            if key is not None or item is not None:
                self.cache_data[key] = item
        except Exception:
            pass

    def get(self, key):
        """Get an item by key"""
        return (
            None
            if key is None or self.cache_data.get(key) is None
            else self.cache_data[key]
        )

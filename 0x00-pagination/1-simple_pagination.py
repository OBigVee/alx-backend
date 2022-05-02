#!/usr/bin/env python3
"""Simple pagination"""
import csv
import math
from typing import List


def index_range(self, page: int, page_size: int) -> tuple:
    """returns a tuple of size two containing and an end index
    corresponding to the range of indexes to return in a list for those particular
    pagination parameters
    """
    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size
    return (startIndex, endIndex)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get appropriate page of dataset"""
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        # deconstructing
        start, end = index_range(self, page, page_size)

        getData = self.dataset()

        result = []

        if start >= len(getData):
            return result
        else:
            return getData[start:end]

#!/usr/bin/env python3
"""Replicate get_page method in '1-simple_pagination.py' """


import csv
import math
from typing import Dict, List


def index_range(page: int, page_size: int) -> tuple:
    """returns a tuple of size two containing a start an end index
    corresponding to the range of indexes to return in the list for
    a particular pagination parameters
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
        start, end = index_range(page, page_size)

        getData = self.dataset()

        result = []

        if start >= len(getData):
            return result
        else:
            return getData[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10):
        """return dictionary contating key-value pairs"""
        data = self.get_page(page, page_size)
        size = len(self.dataset()) // page_size

        if page + 1 < size:
            next_page = page + 1
        else:
            next_page = None

        if page - 1 > 1:
            prev_page = page - 1
        else:
            prev_page = None

        HATEOAS_DATA = {
            "page": page,
            "page_size": page_size,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": size,
        }
        return HATEOAS_DATA

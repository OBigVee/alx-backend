#!/usr/bin/env python3
"""Hypermedia pagination"""
import csv
import math
from typing import List, Tuple


def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
    """function returns a tuple of size two containing a
    start index and an end index corresponding to the
    range of indexes to return in a list for those
    particular pagination parameters"""

    start_index = (page - 1) * page_size  # (1, 2) = 0
    end_index = start_index + page_size  # (0 + 2) = 2
    return (start_index, end_index)


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
        """method takes two int args"""

        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0

        # unpacking
        start, end = index_range(self, page, page_size)
        get_data = self.dataset()
        result: List = []
        # if the input args are out of range for the dataset,return an empty
        # list
        return get_data[start:end] if start < len(get_data) else result

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """method returns a dictionary containing the following key-value
        pairs:
        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer"""
        data = self.get_page(page=page, page_size=page_size)
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

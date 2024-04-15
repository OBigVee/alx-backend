#!/usr/bin/env python3
import csv
from typing import List, Tuple


def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
    """function returns a tuple of size two containing a
    start index and an end index corresponding to the
    range of indexes to return in a list for those
    particular pagination parameters"""

    start_index = (page - 1) * page_size  # (1, 3) = 0
    end_index = start_index + page_size  # (0 + 3) = 3
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
        """method takes two int args
        if the input args are out of range for the dataset,return an empty
        list
        """
        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        start, end = index_range(self, page, page_size)
        get_data = self.dataset()
        result: List = []
        return get_data[start:end] if start < len(get_data) else result

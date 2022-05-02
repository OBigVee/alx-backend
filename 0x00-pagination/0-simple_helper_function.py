#!/usr/bin/env python3
"""simple helper function"""


def index_range(page: int, page_size: int) -> tuple:
    """returns a tuple of size two containing and an end index
    corresponding to the range of indexes to return in a list for those particular
    pagination parameters
    """

    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size
    return (startIndex, endIndex)

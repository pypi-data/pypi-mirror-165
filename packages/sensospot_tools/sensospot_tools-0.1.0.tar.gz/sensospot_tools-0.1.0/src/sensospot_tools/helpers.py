import itertools
from typing import Any

import pandas


def ensure_list(something: Any) -> list[Any]:
    """ensures the provided value is a list or encapsulated in a list

    This is intended to use so that where column names should be provided
    as a list could also be provided as a single column name

    >>> ensure_list("abc")
    ["abc"]

    >>> ensure_list({"a", "b"})
    ["a", "b"]

    >>> ensure_list(1)
    [1]

    something:  the value to be in or the list
    returns:    a list of whatever something is
    """
    # strings are iterables, so here is a special case for them
    if isinstance(something, str):
        return [something]
    try:
        return list(something)
    except TypeError:
        # something is not an iterable
        return [something]


def check_columns_exist(data: pandas.DataFrame, *arguments) -> bool:
    """raises KeyError if columns dont exist in a data frame

    data       : the pandas DataFrame to check for
    *arguments : variatic number of columns or lists of columns to check
    """
    argument_items_as_lists = (ensure_list(arg) for arg in arguments)
    check_cols = set(itertools.chain.from_iterable(argument_items_as_lists))

    if not check_cols.issubset(set(data.columns)):
        unknown_columns = sorted(check_cols.difference(set(data.columns)))
        raise KeyError(f"Unknown column(s): {unknown_columns}")

    return True

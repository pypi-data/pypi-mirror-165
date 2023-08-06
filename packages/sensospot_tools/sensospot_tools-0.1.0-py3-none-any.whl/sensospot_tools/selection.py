from typing import Any, Iterator

import pandas


def select(
    data: pandas.DataFrame, column: str, value: Any
) -> pandas.DataFrame:
    """Selects rows of a dataframe based on a value in a column

    Example:
    >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4

    >>> print(select(data, "category", "cat"))
          category  value
        1      cat      2
        3      cat      4


    data:    a data DataFrame to select from
    column:  name of a column in a dataframe
    value:   rows with this value in the column will be selected
    returns: a copy of the DataFrame that has the value in the column
    """
    selector = data[column] == value
    return data.loc[selector].copy()


def split(
    data: pandas.DataFrame, column: str
) -> Iterator[tuple[Any, pandas.DataFrame]]:
    """Splits a data frame on unique values in a column

    returns an iterator where each result is key-value-pair. The key is the
    unique value used for the split, the value is a slice of the dataframe
    selected by the unique value contained in the column

    Example:

    >>> print(data)
          category  value
        0      dog      1
        1      cat      2
        2    horse      3
        3      cat      4

    >>> result = dict( split(data, column="category") )

    >>> print(result["dog"])
          category  value
        0      dog      1

    >>> print(result["cat"])
          category  value
        1      cat      2
        3      cat      4

    >>> print(result["horse"])
          category  value
        2    horse      3

    data:   DataFrame to process
    column: column identifier to split on unique values
    yields: key-value-pairs of
            keys: one unique value
            values: slice of the dataframe that contains the unique value
    """
    unique_values = data[column].unique()
    return ((value, select(data, column, value)) for value in unique_values)

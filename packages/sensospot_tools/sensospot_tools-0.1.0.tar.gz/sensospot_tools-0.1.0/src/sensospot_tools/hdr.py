from typing import Union

import pandas

from .helpers import ensure_list, check_columns_exist
from .selection import select


def select_hdr_data(
    data: pandas.DataFrame,
    spot_id_columns: Union[list[str], str],
    time_column: str,
    overflow_column: str,
) -> pandas.DataFrame:
    """selects the data for increased dynamic measurement range

    To increase the dynamic range of a measurement, multiple exposures of one
    microarray might be taken.

    This function selects the data of only one exposure time per spot, based
    on the information if the spot is in overflow. It starts with the weakest
    signals (longest exposure time) first and chooses the next lower exposure
    time, if the result in the `overflow_column` is `True`.

    This is done for each spot, and therfore a spot needs a way to be
    identified across multiple exposure times. Examples for this are:
     - for a single array:
       the spot id (e.g. "Pos.Id")
     - for multiple arrays:
       the array position and the spot id (e.g. "Well.Name" and "Pos.Id")
     - for multiple runs:
       the name of the run, array position and the spot id
       (e.g. "File.Name", "Well.Name" and "Pos.Id")

    The function will raise a KeyError if any of the provided column names
    is not present in the data frame

    spot_id_columns: column names identifying a spot
    time_column:     column name for the (nominal) exposure time
    overflow_column: column name holding a overflow test result
    returns:         data frame with selected hdr data per spot
    """

    check_columns_exist(data, spot_id_columns, time_column, overflow_column)
    spot_ids = ensure_list(spot_id_columns)

    sorted_times = sorted(data[time_column].unique(), reverse=True)
    data_by_time = (select(data, time_column, t) for t in sorted_times)
    indexed_data_by_time = (dbt.set_index(spot_ids) for dbt in data_by_time)

    # get the first data set (highest exposure time)
    hdr_data = next(indexed_data_by_time)

    # iterate over the rest of the data sets
    for next_higher_time in indexed_data_by_time:
        selection = hdr_data[overflow_column]
        not_in_overlow = hdr_data.loc[~selection].copy()
        replacement_for_overlow = next_higher_time[selection].copy()
        hdr_data = pandas.concat((not_in_overlow, replacement_for_overlow))

    return hdr_data.reset_index()


def normalize(
    data: pandas.DataFrame,
    normalized_time: Union[int, float],
    time_column: str,
    value_columns: Union[list[str], str],
    template: str = "Normalized.{}",
) -> pandas.DataFrame:
    """normalizes values to a normalized exposure time

    Will raise a KeyError, if any column is not in the data frame;
    raises ValueError if no template string was provided.

    data:            data frame to normalize
    normalized_time: exposure time to normalize to
    time_column:     column name of the (nominal) exposure time
    value_columns:   which columns to normalize
    template:        a Python template string for the normalized column names
    returns:         copy of the data with additional normalized values
    """
    check_columns_exist(data, time_column, value_columns)
    if "{}" not in template:
        raise ValueError(f"Not a template string: '{template}'")

    data = data.copy()

    for column in ensure_list(value_columns):
        normalized_name = template.format(column)
        data[normalized_name] = (
            normalized_time * data[column] / data[time_column]
        )

    return data

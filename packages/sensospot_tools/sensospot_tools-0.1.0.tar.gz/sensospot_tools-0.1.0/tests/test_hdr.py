import pytest

CSV_FULL_DATA = """
spot	time	background	signal	overflow
1	100	1	100	FALSE
1	10	2	200	FALSE
1	1	3	300	FALSE
2	100	4	400	TRUE
2	10	5	500	FALSE
2	1	6	600	FALSE
3	100	7	700	TRUE
3	10	8	800	TRUE
3	1	9	900	FALSE
4	100	10	1000	TRUE
4	10	11	1100	TRUE
4	1	12	1200	TRUE
"""

CSV_ONE_TIME_DATA = """
spot	time	background	signal	overflow
1	100	1	100	TRUE
2	100	2	200	FALSE
3	100	3	300	TRUE
"""

CSV_HDR_DATA = """
spot	time	background	signal	overflow
1	100	1	100	FALSE
2	10	5	500	FALSE
3	1	9	900	FALSE
4	1	12	1200	TRUE
"""

CSV_NORMALIZED_HDR_DATA = """
spot	time	background	signal	overflow	n.background	n.signal
1	100	1	100	FALSE	2	200
2	10	5	500	FALSE	100	1000
3	1	9	900	FALSE	1800	180000
4	1	12	1200	TRUE	2400	240000
"""


def csv_to_data_frame(text):
    import io

    import pandas

    buffer = io.StringIO(text.strip())
    return pandas.read_csv(buffer, sep="\t")


@pytest.fixture
def full_source_data():
    yield csv_to_data_frame(CSV_FULL_DATA)


@pytest.fixture
def one_time_source_data():
    yield csv_to_data_frame(CSV_ONE_TIME_DATA)


@pytest.fixture
def hdr_data():
    yield csv_to_data_frame(CSV_HDR_DATA)


@pytest.fixture
def hdr_normalized_data():
    yield csv_to_data_frame(CSV_HDR_DATA)


def test_select_hdr_data_full_data(full_source_data, hdr_data):
    """select the hdr data from a data frame with multiple exposure times"""
    from sensospot_tools.hdr import select_hdr_data

    result = select_hdr_data(
        data=full_source_data,
        spot_id_columns="spot",
        time_column="time",
        overflow_column="overflow",
    )

    for column in hdr_data.columns:
        assert list(result[column]) == list(hdr_data[column])


def test_select_hdr_data_one_time(one_time_source_data):
    """select the hdr data from a data frame with only one exposure time"""
    from sensospot_tools.hdr import select_hdr_data

    result = select_hdr_data(
        data=one_time_source_data,
        spot_id_columns="spot",
        time_column="time",
        overflow_column="overflow",
    )

    for column in one_time_source_data.columns:
        assert list(result[column]) == list(one_time_source_data[column])


def test_select_hdr_raises_error_on_wrong_column(one_time_source_data):
    from sensospot_tools.hdr import select_hdr_data

    with pytest.raises(KeyError):
        select_hdr_data(
            data=one_time_source_data,
            spot_id_columns="spot",
            time_column="time",
            overflow_column="UNKNOWN",
        )


def test_normalize(hdr_data, hdr_normalized_data):
    from sensospot_tools.hdr import normalize

    result = normalize(
        hdr_data,
        normalized_time=200,
        time_column="time",
        value_columns=["background", "signal"],
        template="n.{}",
    )

    for column in hdr_normalized_data.columns:
        assert list(result[column]) == list(hdr_normalized_data[column])


def test_normalize_raises_error_on_wrong_column(hdr_data):
    from sensospot_tools.hdr import normalize

    with pytest.raises(KeyError):
        normalize(
            hdr_data,
            normalized_time=200,
            time_column="time",
            value_columns=["UNKONWN", "signal"],
        )


def test_normalize_raises_error_no_templae_string(hdr_data):
    from sensospot_tools.hdr import normalize

    with pytest.raises(ValueError):
        normalize(
            hdr_data,
            normalized_time=200,
            time_column="time",
            value_columns="signal",
            template="NO TEMPLATE",
        )

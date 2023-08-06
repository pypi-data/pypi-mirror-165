import pytest


@pytest.mark.parametrize(
    "provided, expected",
    [
        ("abc", ["abc"]),
        (tuple("abc"), ["a", "b", "c"]),
        ({"a": 1, "b": 2}, ["a", "b"]),
        (1, [1]),
    ],
)
def test_helpers_ensure_list(provided, expected):
    from sensospot_tools.helpers import ensure_list

    result = ensure_list(provided)

    assert result == expected


@pytest.mark.parametrize(
    "arguments",
    [
        ("A",),
        ("A", "B"),
        ("B", "C", "D"),
        (["A"], "B", ["C", "D"]),
    ],
)
def test_helpers_check_columns_exist_ok(arguments):
    import pandas

    from sensospot_tools.helpers import check_columns_exist

    columns = ["A", "B", "C", "D"]
    data = pandas.DataFrame({c: [] for c in columns})

    assert check_columns_exist(data, *arguments) is True


def test_helpers_check_columns_exist_raises_error_on_wrong_column():
    import pandas

    from sensospot_tools.helpers import check_columns_exist

    columns = ["A", "B", "C", "D"]
    data = pandas.DataFrame({c: [] for c in columns})

    with pytest.raises(KeyError):
        check_columns_exist(data, "DOES NOT EXIST")

import pytest

CSV_DATA = """
category	value
dog	3
cat	55
horse	35
cat	60
horse	9
"""


@pytest.fixture
def example():
    import io

    import pandas

    buffer = io.StringIO(CSV_DATA.strip())
    yield pandas.read_csv(buffer, sep="\t")


def test_selection_select(example):
    from sensospot_tools.selection import select

    result = select(example, "category", "horse")
    assert list(result["category"]) == ["horse", "horse"]
    assert list(result["value"]) == [35, 9]


def test_selection_split(example):
    from sensospot_tools.selection import split

    result = dict(split(example, "category"))

    assert sorted(result.keys()) == ["cat", "dog", "horse"]
    assert list(result["cat"]["value"]) == [55, 60]
    assert list(result["dog"]["value"]) == [3]
    assert list(result["horse"]["value"]) == [35, 9]

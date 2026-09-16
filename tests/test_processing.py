import pytest
from bank_widget_clean.processing import sort_by_date

@pytest.mark.parametrize(
    "transactions,expected",
    [
        (
            [
                {"id": 2, "date": "2019-07-02T..."},
                {"id": 1, "date": "2019-07-01T..."},
            ],
            [
                {"id": 1, "date": "2019-07-01T..."},
                {"id": 2, "date": "2019-07-02T..."},
            ],
        ),
    ],
)
def test_sort_by_date(transactions, expected):
    assert sort_by_date(transactions) == expected
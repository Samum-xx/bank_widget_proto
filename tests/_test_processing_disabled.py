import pytest

from src.processing import process_transactions


@pytest.mark.parametrize("input_data,expected_count", [
    ([], 0),
    ([{"amount": 100}], 1),
])
def test_process_transactions_basic(input_data, expected_count):
    result = process_transactions(input_data)
    assert len(result) == expected_count


def test_process_transactions_with_filter():
    data = [
        {"amount": 100, "currency": "USD"},
        {"amount": 200, "currency": "RUB"},
    ]
    result = process_transactions(data, min_amount=150)
    assert len(result) == 1
    assert result[0]["amount"] == 200

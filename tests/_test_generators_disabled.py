from unittest.mock import patch

from generators import generate_transactions


@patch("generators.random.randint", return_value=100)
def test_generate_transactions_count(mock_randint):
    transactions = generate_transactions(5)
    assert len(transactions) == 5
    assert all("amount" in t for t in transactions)


@patch("generators.random.choice", side_effect=["USD", "EUR", "RUB"])
def test_generate_transactions_currencies(mock_choice):
    transactions = generate_transactions(3)
    currencies = [t["currency"] for t in transactions]
    assert currencies == ["USD", "EUR", "RUB"]


def test_generate_transactions_amount_range():
    transactions = generate_transactions(10)
    for t in transactions:
        assert 50 <= t["amount"] <= 5000


@patch("generators.datetime.now")
def test_generate_transactions_dates(mock_now):
    mock_now.return_value.strftime.return_value = "2024-01-01"
    transactions = generate_transactions(2)
    for t in transactions:
        assert t["date"] == "2024-01-01"

from generators.filter_by_currency import filter_by_currency


def test_filter_by_currency_returns_iterator():
    transactions = [
        {"currency": "RUB", "amount": 100},
        {"currency": "USD", "amount": 200},
    ]
    result = filter_by_currency(transactions, "RUB")
    assert list(result) == [{"currency": "RUB", "amount": 100}]


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "RUB")) == []


def test_filter_by_currency_no_matches():
    transactions = [{"currency": "USD", "amount": 500}]
    assert list(filter_by_currency(transactions, "RUB")) == []
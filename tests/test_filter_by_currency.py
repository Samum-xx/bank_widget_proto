import pytest
from generators.filter_by_currency import filter_by_currency

from src.external_api import convert_to_rub


def test_convert_usd_to_rub():
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rub(transaction, rate_override=90.5)
    assert result == pytest.approx(9050.0)


def test_convert_eur_to_rub():
    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_to_rub(transaction, rate_override=100.2)
    assert result == pytest.approx(5010.0)


def test_convert_rub_no_api():
    transaction = {"amount": 1500, "currency": "RUB"}
    result = convert_to_rub(transaction)
    # Если convert_to_rub для RUB просто возвращает amount, то это сработает
    assert result == 1500.0


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

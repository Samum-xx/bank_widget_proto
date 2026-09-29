import pytest
from unittest.mock import patch
from src.external_api import convert_to_rub

def test_convert_usd_to_rub():
    transaction = {"amount": 100, "currency": "USD"}
    # Передаём курс напрямую — тест проверяет логику умножения
    result = convert_to_rub(transaction, rate_override=90.5)
    assert result == pytest.approx(9050.0)

def test_convert_eur_to_rub():
    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_to_rub(transaction, rate_override=100.2)
    assert result == pytest.approx(5010.0)

def test_convert_rub_no_api():
    transaction = {"amount": 1500, "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 1500.0

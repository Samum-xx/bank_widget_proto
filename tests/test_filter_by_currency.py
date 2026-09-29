import pytest
from unittest.mock import patch
from src.external_api import convert_to_rub
from src.utils import read_json_file  # <-- было load_transactions_from_json, стало read_json_file

@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get):
    mock_response = type('Response', (object,), {'json': lambda self: {"result": 90.5}})()
    mock_get.return_value = mock_response
    assert convert_to_rub({"amount": 100, "currency": "USD"}) == pytest.approx(9050.0)

@patch("src.external_api.requests.get")
def test_convert_eur_to_rub(mock_get):
    mock_response = type('Response', (object,), {'json': lambda self: {"result": 100.2}})()
    mock_get.return_value = mock_response
    assert convert_to_rub({"amount": 50, "currency": "EUR"}) == pytest.approx(5010.0)

def test_convert_rub_no_api():
    assert convert_to_rub({"amount": 1500, "currency": "RUB"}) == 1500.0

from unittest.mock import patch, Mock
import requests
from src.external_api import convert_to_rub


@patch("src.external_api.API_KEY", "test_key")
def test_convert_to_rub_rub():
    """Если валюта RUB — просто возвращаем сумму как float."""
    transaction = {"amount": 1500, "currency": "RUB"}
    assert convert_to_rub(transaction) == 1500.0


@patch("src.external_api.API_KEY", "test_key")
@patch("requests.get")
def test_convert_to_rub_usd_success(mock_get):
    """USD: успешный ответ API — конвертируем по курсу."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value={"rates": {"USD": 1.0}})
    mock_get.return_value = mock_response
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_to_rub(transaction)
    assert isinstance(result, float)
    assert result == 100.0


@patch("src.external_api.API_KEY", "test_key")
@patch("requests.get")
def test_convert_to_rub_eur_success(mock_get):
    """EUR: успешный ответ — конвертируем."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value={"rates": {"EUR": 0.92}})
    mock_get.return_value = mock_response
    transaction = {"amount": 200, "currency": "EUR"}
    result = convert_to_rub(transaction)
    assert isinstance(result, float)
    assert result == 184.0


@patch("src.external_api.API_KEY", "")
def test_convert_to_rub_no_key():
    """Нет API_KEY — функция должна безопасно вернуть исходную сумму."""
    transaction = {"amount": 300, "currency": "USD"}
    assert convert_to_rub(transaction) == 300.0


@patch("src.external_api.API_KEY", "test_key")
@patch("requests.get", side_effect=requests.exceptions.RequestException)
def test_convert_to_rub_network_error(mock_get):
    """Ошибка сети — безопасно возвращаем исходную сумму."""
    transaction = {"amount": 400, "currency": "USD"}
    assert convert_to_rub(transaction) == 400.0


@patch("src.external_api.API_KEY", "test_key")
@patch("requests.get")
def test_convert_to_rub_unknown_rate(mock_get):
    """API ответил, но курс для валюты не найден — безопасно возвращаем сумму."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value={"rates": {}})
    mock_get.return_value = mock_response
    transaction = {"amount": 500, "currency": "USD"}
    assert convert_to_rub(transaction) == 500.0

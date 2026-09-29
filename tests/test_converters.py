import pytest
from unittest.mock import patch, MagicMock
from src.converters import convert_to_rub

@patch("src.converters.requests.get")
def test_convert_to_rub_success(mock_get):
    """Тест: успешный ответ от API, конвертация работает."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "rates": {"RUB": 90.5},
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_to_rub(100.0, "USD")

    assert result == 9050.0
    mock_get.assert_called_once()


@patch("src.converters.requests.get")
def test_convert_to_rub_network_error(mock_get):
    """Тест: ошибка сети — функция возвращает исходную сумму."""
    from requests.exceptions import RequestException
    mock_get.side_effect = RequestException("Connection failed")

    result = convert_to_rub(200.0, "EUR")

    assert result == 200.0  # Вернули как есть
    mock_get.assert_called_once()


@patch("src.converters.requests.get")
def test_convert_to_rub_missing_rate(mock_get):
    """Тест: API ответил, но RUB нет в rates — возвращаем исходную сумму."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 1.2}}  # RUB нет
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_to_rub(50.0, "EUR")

    assert result == 50.0
    mock_get.assert_called_once()

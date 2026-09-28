import json
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_valid_list():
    """Успешный случай: JSON — это список словарей."""
    data = [
        {"amount": 100.0, "currency": "RUB"},
        {"amount": 50.0, "currency": "USD"},
    ]
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        result = read_json_file("dummy.json")
    assert result == data


def test_read_json_file_not_found():
    """Файл не найден — функция должна вернуть пустой список."""
    result = read_json_file("nonexistent.json")
    assert result == []


def test_read_json_file_empty():
    """Пустой файл — должен вернуть пустой список."""
    m = mock_open(read_data="")
    with patch("builtins.open", m):
        result = read_json_file("empty.json")
    assert result == []


def test_read_json_file_invalid_json():
    """Невалидный JSON — должен вернуть пустой список."""
    m = mock_open(read_data="{not valid json}")
    with patch("builtins.open", m):
        result = read_json_file("bad.json")
    assert result == []


def test_read_json_file_not_list():
    """JSON есть, но это не список (например, словарь) — должен вернуть пустой список."""
    data = {"total": 12345}
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        result = read_json_file("dict.json")
    assert result == []

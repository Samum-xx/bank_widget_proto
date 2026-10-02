import json

import pytest

from src.utils import load_operations


def test_load_operations_valid_file(tmp_path):
    """Тест: корректный JSON-файл возвращает список операций."""
    data = [
        {"id": 1, "amount": 100.0, "currency": "USD"},
        {"id": 2, "amount": 200.5, "currency": "EUR"},
    ]
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_operations(str(file_path))
    assert result == data
    assert isinstance(result, list)


def test_load_operations_missing_file():
    """Тест: если файла нет — возвращается пустой список."""
    result = load_operations("data/nonexistent_file.json")
    assert result == []


def test_load_operations_invalid_json(tmp_path):
    """Тест: битый JSON — возвращается пустой список."""
    file_path = tmp_path / "bad.json"
    # Невалидный JSON специально
    file_path.write_text("{ not valid json }", encoding="utf-8")
    result = load_operations(str(file_path))
    assert result == []


def test_load_operations_not_list(tmp_path):
    """Тест: файл есть, JSON валидный, но не список — возвращается пустой список."""
    file_path = tmp_path / "not_list.json"
    file_path.write_text(json.dumps({"amount": 100, "currency": "RUB"}), encoding="utf-8")
    result = load_operations(str(file_path))
    assert result == []

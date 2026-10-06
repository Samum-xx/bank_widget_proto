import json
from unittest.mock import MagicMock, patch

import pytest

from src.utils import load_operations, read_csv_transactions, read_excel_transactions

# --- Тесты для load_operations (JSON) ---

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
    file_path.write_text("{ not valid json }", encoding="utf-8")
    result = load_operations(str(file_path))
    assert result == []


def test_load_operations_not_list(tmp_path):
    """Тест: файл есть, JSON валидный, но не список — возвращается пустой список."""
    file_path = tmp_path / "not_list.json"
    file_path.write_text(json.dumps({"amount": 100, "currency": "RUB"}), encoding="utf-8")
    result = load_operations(str(file_path))
    assert result == []


# --- Тесты для CSV (с Mock/patch) ---

@patch("src.utils.utils.Path")
@patch("src.utils.utils.pd.read_csv")
def test_read_csv_transactions_success(mock_read_csv, mock_path_class):
    """Успешное чтение CSV: pandas вызван, результат — список словарей."""
    mock_instance = MagicMock()
    mock_instance.exists.return_value = True
    mock_path_class.return_value = mock_instance

    mock_df = MagicMock()
    mock_df.empty = False
    expected_data = [{"amount": 100, "currency": "USD"}]
    mock_df.to_dict.return_value = expected_data
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("test.csv")

    assert result == expected_data
    mock_read_csv.assert_called_once()
    mock_df.to_dict.assert_called_once_with(orient="records")


@patch("src.utils.utils.Path")
def test_read_csv_transactions_file_not_found(mock_path_class):
    """Файл не найден — должна выброситься FileNotFoundError."""
    instance = MagicMock()
    instance.exists.return_value = False
    mock_path_class.return_value = instance

    with pytest.raises(FileNotFoundError):
        read_csv_transactions("nonexistent.csv")


@patch("src.utils.utils.Path")
@patch("src.utils.utils.pd.read_csv")
def test_read_csv_transactions_empty_file(mock_read_csv, mock_path_class):
    """Пустой CSV — должен вернуться пустой список."""
    mock_instance = MagicMock()
    mock_instance.exists.return_value = True
    mock_path_class.return_value = mock_instance

    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("empty.csv")
    assert result == []
    mock_read_csv.assert_called_once()


# --- Тесты для Excel (с Mock/patch) ---

@patch("src.utils.utils.Path")
@patch("src.utils.utils.pd.read_excel")
def test_read_excel_transactions_success(mock_read_excel, mock_path_class):
    """Успешное чтение Excel: pandas вызван, результат — список словарей."""
    mock_instance = MagicMock()
    mock_instance.exists.return_value = True
    mock_path_class.return_value = mock_instance

    mock_df = MagicMock()
    mock_df.empty = False
    expected_data = [{"amount": 200, "currency": "RUB"}]
    mock_df.to_dict.return_value = expected_data
    mock_read_excel.return_value = mock_df

    result = read_excel_transactions("test.xlsx")

    assert result == expected_data
    mock_read_excel.assert_called_once()
    mock_df.to_dict.assert_called_once_with(orient="records")


@patch("src.utils.utils.Path")
def test_read_excel_transactions_file_not_found(mock_path_class):
    """Файл Excel не найден — FileNotFoundError."""
    instance = MagicMock()
    instance.exists.return_value = False
    mock_path_class.return_value = instance

    with pytest.raises(FileNotFoundError):
        read_excel_transactions("nonexistent.xlsx")


@patch("src.utils.utils.Path")
@patch("src.utils.utils.pd.read_excel")
def test_read_excel_transactions_empty_file(mock_read_excel, mock_path_class):
    """Пустой Excel — пустой список."""
    mock_instance = MagicMock()
    mock_instance.exists.return_value = True
    mock_path_class.return_value = mock_instance

    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_excel.return_value = mock_df

    result = read_excel_transactions("empty.xlsx")
    assert result == []
    mock_read_excel.assert_called_once()

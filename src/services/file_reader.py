import csv
from pathlib import Path
from typing import Any, Dict, List


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Функция открывает CSV-файл, проверяет наличие заголовков и возвращает
    список словарей, где каждый словарь — одна транзакция. Значения строк
    автоматически очищаются от лишних пробелов.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если путь не является файлом или файл пуст/не содержит заголовков.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    if not path.is_file():
        raise ValueError(f"Путь не является файлом: {file_path}")

    transactions: List[Dict[str, Any]] = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV-файл пуст или не содержит заголовков.")

        for row in reader:
            clean_row = {
                k.strip(): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
            }
            # Добавляем строку, только если в ней есть хоть какие-то непустые значения
            if any(clean_row.values()):
                transactions.append(clean_row)

    return transactions

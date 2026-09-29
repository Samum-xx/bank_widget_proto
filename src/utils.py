import json
from pathlib import Path
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    Если файл не найден, пустой, содержит не список или некорректный JSON —
    возвращается пустой список.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей (транзакций) или пустой список при ошибке.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    if not isinstance(data, list):
        return []

    return data

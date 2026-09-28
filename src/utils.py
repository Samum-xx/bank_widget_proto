import json
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.
    Args:
        file_path (str): Путь к JSON-файлу.
    Returns:
        List[Dict[str, Any]]: Список словарей (транзакций) или пустой список при ошибке.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
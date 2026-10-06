import json
from typing import Any, List


def read_json_file(filename: str) -> List[Any]:
    """
    Читает JSON-файл и возвращает список операций.
    Если файл не найден или данные не являются списком — возвращает пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

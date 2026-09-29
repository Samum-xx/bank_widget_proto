import json
from pathlib import Path
from typing import List, Dict, Any


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список операций из JSON-файла.

    Если файл не найден, повреждён, содержит не список или имеет неверный формат JSON,
    функция безопасно возвращает пустой список.

    Args:
        file_path (str): Путь к JSON-файлу с операциями.

    Returns:
        List[Dict[str, Any]]: Список словарей с операциями или пустой список при любой ошибке.
    """
    path = Path(file_path)

    # Сначала проверяем, существует ли файл — это экономит ресурсы и даёт понятный поток
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # Сюда попадают и проблемы с чтением, и битый JSON
        return []

    # Гарантируем, что возвращаем только список
    if isinstance(data, list):
        return data

    return []

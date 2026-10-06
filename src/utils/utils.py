import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

MODULE_NAME = "utils"
LOG_FILE = "utils.log"

logger = logging.getLogger(MODULE_NAME)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_json_file(path: str) -> Dict[str, Any]:
    """Считывает JSON-файл и возвращает словарь с данными.

    Args:
        path: Путь к JSON-файлу.

    Returns:
        Словарь с данными из файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если содержимое файла не является словарем.
    """
    file_path = Path(path)

    if not file_path.exists():
        msg = f"JSON file not found: {path}"
        logger.error(msg, exc_info=True)
        raise FileNotFoundError(msg)

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            msg = f"Expected dict in {path}, got {type(data).__name__}"
            logger.error(msg)
            raise ValueError(msg)

        logger.info("Successfully read JSON file: %s", path)
        return data

    except (json.JSONDecodeError, OSError) as e:
        msg = f"Failed to parse JSON in {path}: {e}"
        logger.error(msg, exc_info=True)
        raise


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """Загружает финансовые операции из JSON-файла.

    Если файл не найден или повреждён, возвращает пустой список.

    Args:
        file_path: Путь к JSON-файлу с операциями.

    Returns:
        Список словарей с транзакциями.
    """
    path = Path(file_path)

    if not path.exists():
        logger.warning("Operations file not found, returning empty list: %s", file_path)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(
            "Failed to load operations from %s: %s", file_path, e, exc_info=True
        )
        return []

    if isinstance(data, list):
        return data

    logger.warning(
        "Operations file does not contain a list, returning empty list: %s", file_path
    )
    return []


def read_csv_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        path: Путь к CSV-файлу.

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл пуст или не может быть прочитан.
    """
    file_path = Path(path)

    if not file_path.exists():
        msg = f"CSV file not found: {path}"
        logger.error(msg, exc_info=True)
        raise FileNotFoundError(msg)

    try:
        df = pd.read_csv(file_path, sep=";")
        if df.empty:
            logger.warning("CSV file is empty: %s", path)
            return []

        result: List[Dict[str, Any]] = df.to_dict(orient="records")
        logger.info("Successfully read CSV file: %s, rows=%d", path, len(result))
        return result

    except Exception as e:
        msg = f"Failed to parse CSV file {path}: {e}"
        logger.error(msg, exc_info=True)
        raise ValueError(msg) from e


def read_excel_transactions(path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx).

    Args:
        path: Путь к XLSX-файлу.

    Returns:
        Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если файл пуст или не может быть прочитан.
    """
    file_path = Path(path)

    if not file_path.exists():
        msg = f"Excel file not found: {path}"
        logger.error(msg, exc_info=True)
        raise FileNotFoundError(msg)

    try:
        df = pd.read_excel(file_path)
        if df.empty:
            logger.warning("Excel file is empty: %s", path)
            return []

        result: List[Dict[str, Any]] = df.to_dict(orient="records")
        logger.info("Successfully read Excel file: %s, rows=%d", path, len(result))
        return result

    except Exception as e:
        msg = f"Failed to parse Excel file {path}: {e}"
        logger.error(msg, exc_info=True)
        raise ValueError(msg) from e

import json
from pathlib import Path
from typing import Any, Dict, List

from src.utils.logging_setup import get_logger

logger = get_logger("utils", "utils.log", "INFO")


def read_json_file(path: str) -> Dict[str, Any]:
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
    path = Path(file_path)

    if not path.exists():
        logger.warning("Operations file not found, returning empty list: %s", file_path)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to load operations from %s: %s", file_path, e, exc_info=True)
        return []

    if isinstance(data, list):
        return data

    logger.warning("Operations file does not contain a list, returning empty list: %s", file_path)
    return []

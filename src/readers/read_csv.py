import csv
import logging
from pathlib import Path
from typing import Any, Dict, List

MODULE_NAME = "readers.csv"
logger = logging.getLogger(MODULE_NAME)

if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("readers.log", encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_csv(path: str) -> List[Dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        msg = f"CSV file not found: {path}"
        logger.error(msg, exc_info=True)
        raise FileNotFoundError(msg)

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        result: List[Dict[str, Any]] = list(reader)

    logger.info("Successfully read CSV file: %s, rows=%d", path, len(result))
    return result

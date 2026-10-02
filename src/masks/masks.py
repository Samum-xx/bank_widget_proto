import logging
from pathlib import Path

MODULE_NAME = "masks"
LOG_FILE = "masks.log"

# Создаём логгер
logger = logging.getLogger(MODULE_NAME)
logger.setLevel(logging.DEBUG)  # не меньше DEBUG

# FileHandler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Formatter: время, модуль, уровень, сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логгеру
if not logger.handlers:  # защита от дублирования при множественных импортах
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    if not card_number or not card_number.isdigit() or len(card_number) < 16:
        logger.warning("Некорректный номер карты: %s", card_number)
        return "Некорректный номер карты"

    digits = card_number.replace(" ", "")
    masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    logger.info("Замаскирован номер карты: %s -> %s", card_number, masked)
    return masked


def get_mask_account(account_number: str) -> str:
    if not account_number or not account_number.isdigit() or len(account_number) < 4:
        logger.warning("Некорректный номер счёта: %s", account_number)
        return "Некорректный номер счёта"

    result = f"**{account_number[-4:]}"
    logger.info("Замаскирован номер счёта: %s -> %s", account_number, result)
    return result

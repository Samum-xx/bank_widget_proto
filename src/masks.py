import logging
from pathlib import Path

MODULE_NAME = "masks"
LOG_FILE = "masks.log"

# Создаём логгер
logger = logging.getLogger(MODULE_NAME)

# Если у логгера уже есть хендлеры — не добавляем второй (защита от дублирования)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)

    # FileHandler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Formatter: время, модуль, уровень, сообщение
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты по шаблону: XXXX XX** **** XXXX.

    Args:
        card_number: строка с номером карты (могут быть пробелы).

    Returns:
        Замаскированный номер или сообщение об ошибке.
    """
    if not card_number:
        logger.warning("Получен пустой номер карты.")
        return "Некорректный номер карты"

    digits = card_number.replace(" ", "")

    if not digits.isdigit() or len(digits) < 16:
        logger.warning("Некорректный номер карты: %s", card_number)
        return "Некорректный номер карты"

    # Берём последние 4 цифры, остальное маскируем
    masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    logger.info("Замаскирован номер карты: %s -> %s", card_number, masked)
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.

    Args:
        account_number: строка с номером счёта.

    Returns:
        Замаскированный счёт или сообщение об ошибке.
    """
    if not account_number:
        logger.warning("Получен пустой номер счёта.")
        return "Некорректный номер счёта"

    digits = account_number.replace(" ", "")

    if not digits.isdigit() or len(digits) < 4:
        logger.warning("Некорректный номер счёта: %s", account_number)
        return "Некорректный номер счёта"

    result = f"**{digits[-4:]}"
    logger.info("Замаскирован номер счёта: %s -> %s", account_number, result)
    return result

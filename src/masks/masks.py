from src.utils.logging_setup import get_logger

logger = get_logger("masks", "masks.log", "INFO")


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
        logger.warning("Некорректный номер счета: %s", account_number)
        return "Некорректный номер счета"

    result = f"**{account_number[-4:]}"
    logger.info("Замаскирован номер счета: %s -> %s", account_number, result)
    return result

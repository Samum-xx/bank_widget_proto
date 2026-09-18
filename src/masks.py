"""Модуль masks — функции для маскировки номеров карт и счетов."""


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты строкой и возвращает замаскированный номер.

    Формат: XXXX XX** **** XXXX
    Пример: 7000792289606361 -> 7000 79** **** 6361

    Args:
        card_number: номер карты строкой (без пробелов).

    Returns:
        Замаскированный номер карты.
    """
    if not card_number or not card_number.isdigit() or len(card_number) < 16:
        return "Некорректный номер карты"

    digits = card_number.replace(" ", "")
    masked = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета строкой и возвращает замаскированный номер.

    Формат: **XXXX
    Пример: 73654108430135874305 -> **4305

    Args:
        account_number: номер счета строкой (без пробелов).

    Returns:
        Замаскированный номер счета.
    """
    if not account_number or not account_number.isdigit() or len(account_number) < 4:
        return "Некорректный номер счета"

    return f"**{account_number[-4:]}"
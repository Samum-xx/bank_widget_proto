"""Модуль widget — функции для маскировки номеров карт/счетов и форматирования дат."""

from src.masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not info or not info.strip():
        raise ValueError("Передана пустая строка")

    parts = info.strip().split()
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер")

    if not parts[-1].isdigit():
        raise ValueError("Последняя часть строки должна быть числом")

    if len(parts) > 2 and parts[-2].isdigit():
        raise ValueError("Строка содержит слишком много числовых подстрок")

    if parts[0].lower() == "счет":
        account_number = parts[-1]
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        card_name = " ".join(parts[:-1])
        card_number = parts[-1]
        masked_number = get_mask_card_number(card_number)
        return f"{card_name} {masked_number}"


def get_date(date_string: str) -> str:
    """Принимает строку с датой в ISO-формате и возвращает дату в формате ДД.ММ.ГГГГ."""
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
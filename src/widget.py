"""Модуль widget — функции для маскировки номеров карт/счетов и форматирования дат."""


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


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в переданной строке.

    Различает карту и счет по наличию слова 'Счет' (без учёта регистра).
    Для карт использует get_mask_card_number, для счетов — get_mask_account.

    Args:
        info: строка вида 'Visa Platinum 7000792289606361' или 'Счет 73654108430135874305'.

    Returns:
        Строка с замаскированным номером.

    Raises:
        ValueError: если передана пустая строка или строка содержит больше 2 частей
            (имя + номер), которые не удается корректно разобрать.
    """
    if not info or not info.strip():
        raise ValueError("Передана пустая строка")

    parts = info.strip().split()

    # Защита от некорректного ввода: строка должна содержать хотя бы 2 части
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер")

    # Проверяем, что последняя часть — это цифры (номер)
    if not parts[-1].isdigit():
        raise ValueError("Последняя часть строки должна быть числом")

    # Если предпоследнее слово тоже часть номера (число),
    # а вся строка содержит слишком много числовых подстрок — это некорректный ввод
    if len(parts) > 2 and parts[-2].isdigit():
        raise ValueError("Строка содержит слишком много числовых подстрок")

    # Определяем, счёт это или карта
    if parts[0].lower() == "счет":
        # Для счета: имя — "Счет", номер — всё остальное
        account_number = parts[-1]
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        # Для карты: имя — всё кроме последней части, номер — последняя часть
        card_name = " ".join(parts[:-1])
        card_number = parts[-1]
        masked_number = get_mask_card_number(card_number)
        return f"{card_name} {masked_number}"


def get_date(date_string: str) -> str:
    """Принимает строку с датой в ISO-формате и возвращает дату в формате ДД.ММ.ГГГГ.

    Пример: '2024-03-11T02:26:18.671407' -> '11.03.2024'

    Args:
        date_string: строка даты в ISO-формате (например, '2024-03-11T02:26:18.671407').

    Returns:
        Строка с датой в формате ДД.ММ.ГГГГ.
    """
    from datetime import datetime

    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
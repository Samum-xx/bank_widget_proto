from typing import List, Dict, Any
from src.masks import get_mask_card_number


def get_last_successful_operations(operations: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    successful = [op for op in operations if op.get("status") == "SUCCESS"]
    successful.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return successful[:limit]


def format_operation_for_display(operation: Dict[str, Any]) -> str:
    amount = operation.get("amount", 0)
    currency = operation.get("currency", "RUB")
    timestamp = operation.get("timestamp", "")

    date_str = timestamp[:10] if timestamp else "??.??.????"
    if len(date_str) == 10:
        try:
            parts = date_str.split("-")
            date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
        except Exception:
            pass

    return f"{date_str}: Оплата на {amount:,.0f} ₽ — Успешно"


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счёта в строке вида:
      - 'Visa Platinum 7000792289606361'
      - 'Счет 73654108430135874305'

    Для карт использует get_mask_card_number из masks.py.
    Для счетов оставляет последние 4 цифры, остальное заменяет на '*'.
    """
    # Ищем, где начинается номер (первая цифра после пробела)
    # Предполагаем, что тип (Visa, Счет и т.п.) отделён от номера пробелом
    parts = info.rsplit(" ", 1)  # разбиваем только по последнему пробелу

    if len(parts) != 2:
        # Если нет пробела, возвращаем как есть или можно выбросить ошибку
        return info

    prefix, number_raw = parts

    # Проверяем, похоже ли это на счёт
    if prefix.lower() == "счет":
        # Для счёта: оставляем последние 4 цифры
        clean_number = "".join(c for c in number_raw if c.isdigit())
        if len(clean_number) <= 4:
            masked_number = clean_number
        else:
            masked_number = "*" * (len(clean_number) - 4) + clean_number[-4:]
        return f"{prefix} {masked_number}"

    # Иначе считаем это картой и используем существующую функцию
    try:
        masked_card = get_mask_card_number(number_raw)
        return f"{prefix} {masked_card}"
    except ValueError:
        # Если номер слишком короткий, можно вернуть как есть или с предупреждением
        return f"{prefix} {number_raw}"


def get_date(iso_string: str) -> str:
    """
    Преобразует строку даты в формате ISO (2024-03-11T02:26:18.671407)
    в формат ДД.ММ.ГГГГ (11.03.2024).
    """
    # Берём первые 10 символов: YYYY-MM-DD
    date_part = iso_string[:10]
    if len(date_part) != 10 or date_part[4] != "-" or date_part[7] != "-":
        return iso_string  # если формат не совпадает, возвращаем как есть

    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
# widget.py — тут я собираю данные для виджета с операциями.
#
# 1. mask_card_number — берёт номер карты, убирает пробелы/дефисы, проверяет,
#    что остались только цифры и их хотя бы 16 штук. Потом прячет всё, кроме последних 4.
#    Если что-то не так — кидает ошибку, чтобы дальше не ломать.
# 2. prepare_operations_widget_data — собирает готовый список операций для показа:
#    - берёт только успешные (status == "success"),
#    - сортирует от новых к старым,
#    - оставляет только первые N штук (по умолчанию 5),
#    - для каждой маскирует карту и собирает простой словарь под интерфейс.
#
# Каждую часть можно отдельно проверить тестами.

from typing import List, Dict, Any


def mask_card_number(card_number: str) -> str:
    """
    Чистит номер карты и делает маску.
    """
    # Убираю пробелы и дефисы — пользователь мог ввести как угодно
    cleaned = card_number.replace(" ", "").replace("-", "")

    # Проверяю, что остались только цифры
    if not cleaned.isdigit():
        raise ValueError("Card number must contain only digits after cleaning.")

    # Проверяю минимальную длину — иначе маска не имеет смысла
    if len(cleaned) < 16:
        raise ValueError("Card number is too short.")

    # Беру последние 4 цифры, остальное прячу
    last_four = cleaned[-4:]
    return f"XXXX XXXX XXXX {last_four}"


def prepare_operations_widget_data(
    operations: List[Dict[str, Any]],
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Подготавливает список операций для виджета: фильтрует, сортирует,
    ограничивает количество и маскирует карты.
    """

    # Шаг 1: оставляю только успешные операции — чтобы в виджете не было ошибок
    successful = [op for op in operations if op.get("status") == "success"]

    # Шаг 2: сортирую от новых к старым по полю created_at
    sorted_ops = sorted(
        successful,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    # Шаг 3: беру только первые limit штук и для каждой делаю маску карты
    result = []
    for op in sorted_ops[:limit]:
        # Маскирую номер карты через отдельную функцию
        card_masked = mask_card_number(op["card_number"])

        # Собираю простой словарь с полями, которые нужны интерфейсу
        result.append({
            "id": op["id"],
            "amount": op["amount"],
            # Если валюты нет — ставлю RUB по умолчанию
            "currency": op.get("currency", "RUB"),
            # Если описания нет — ставлю заглушку
            "description": op.get("description", "Операция"),
            "card_masked": card_masked,
            "created_at": op["created_at"],
        })

    return result
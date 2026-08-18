from typing import List, Dict, Any


def mask_card_number(card_number: str) -> str:
    """
    Чистит номер карты и делает маску.
    Оставляет только цифры, требует минимум 16 символов, возвращает XXXX XXXX XXXX ****
    """
    # Убираем пробелы и дефисы
    cleaned = card_number.replace(" ", "").replace("-", "")

    if not cleaned.isdigit():
        raise ValueError("Card number must contain only digits after cleaning.")

    if len(cleaned) < 16:
        raise ValueError("Card number is too short.")

    last_four = cleaned[-4:]
    return f"XXXX XXXX XXXX {last_four}"


def prepare_operations_widget_data(
    operations: List[Dict[str, Any]],
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Подготавливает список операций для виджета:
      - фильтрует только успешные (status == "success")
      - сортирует от новых к старым по created_at
      - ограничивает количество (limit)
      - маскирует номер карты
    """
    # Фильтруем успешные операции
    successful = [op for op in operations if op.get("status") == "success"]

    # Сортируем от новых к старым
    sorted_ops = sorted(
        successful,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    # Берём первые limit штук и собираем результат
    result = []
    for op in sorted_ops[:limit]:
        card_masked = mask_card_number(op["card_number"])

        result.append({
            "id": op["id"],
            "amount": op["amount"],
            "currency": op.get("currency", "RUB"),
            "description": op.get("description", "Операция"),
            "card_masked": card_masked,
            "created_at": op["created_at"],
        })

    return result
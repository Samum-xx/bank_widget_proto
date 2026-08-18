from typing import List, Dict, Any


def mask_card_number(card_number: str) -> str:
    """
    Очищает номер карты от пробелов и дефисов, проверяет, что остались только цифры,
    и что длина не меньше 16. Возвращает маску: XXXX XXXX XXXX XXXX.
    """
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
      - фильтрует успешные операции (status == "success"),
      - сортирует по времени (created_at) от новых к старым,
      - берёт первые limit операций,
      - маскирует номера карт.
    Возвращает список словарей с полями, нужными для UI.
    """
    successful = [op for op in operations if op.get("status") == "success"]

    sorted_ops = sorted(
        successful,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

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
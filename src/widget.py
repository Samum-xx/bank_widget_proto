from typing import List, Dict, Any


def get_last_successful_operations(operations: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает последние успешные операции в порядке от новых к старым.

    Параметры:
        operations: список всех операций клиента (каждая операция — dict)
        limit: сколько операций вернуть (по умолчанию 5)

    Пример операции:
        {
            "id": 123,
            "amount": 500.0,
            "currency": "RUB",
            "status": "SUCCESS",
            "timestamp": "2024-06-01T12:34:56Z"
        }
    """
    # Фильтруем только успешные
    successful = [op for op in operations if op.get("status") == "SUCCESS"]

    # Сортируем по времени (предполагаем, что timestamp можно сравнивать как строку или datetime)
    # Если у тебя timestamp — строка ISO, лексикографический порядок обычно совпадает с хронологическим
    successful.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    return successful[:limit]


def format_operation_for_display(operation: Dict[str, Any]) -> str:
    """
    Форматирует одну операцию для показа в виджете.
    Пример вывода: "12.06.2024: Оплата на 1 250 ₽ — Успешно"
    """
    amount = operation.get("amount", 0)
    currency = operation.get("currency", "RUB")
    timestamp = operation.get("timestamp", "")

    # Простая обработка даты: берём первые 10 символов (YYYY-MM-DD) и меняем на DD.MM.YYYY
    date_str = timestamp[:10] if timestamp else "??.??.????"
    if len(date_str) == 10:
        try:
            parts = date_str.split("-")
            date_str = f"{parts[2]}.{parts[1]}.{parts[0]}"
        except Exception:
            pass

    return f"{date_str}: Оплата на {amount:,.0f} ₽ — Успешно"
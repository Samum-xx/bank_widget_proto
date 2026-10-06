from typing import Any, Dict, List


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Оставляет только транзакции с указанным статусом."""
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(
    transactions: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате. По умолчанию новые сначала."""

    def get_date_key(tx: Dict[str, Any]) -> str:
        # Если даты нет — возвращаем пустую строку, она встанет в конец при сортировке
        return str(tx.get("date", ""))

    return sorted(transactions, key=get_date_key, reverse=reverse)

# src/processing.py

def filter_by_state(transactions, state="EXECUTED"):
    """Оставляет только транзакции с указанным статусом."""
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions, reverse=True):
    """Сортирует транзакции по дате. По умолчанию новые сначала."""
    return sorted(transactions, key=lambda x: x.get("date"), reverse=reverse)
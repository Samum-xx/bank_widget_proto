def filter_by_state(transactions, state):
    """Фильтрует транзакции по заданному состоянию."""
    return [trans for trans in transactions if trans['state'] == state]

def sort_by_date(transactions):
    """Сортирует транзакции по дате."""
    return sorted(transactions, key=lambda x: x['date'])
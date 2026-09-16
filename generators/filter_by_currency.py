def filter_by_currency(transactions, currency):
    """
    Возвращает итератор по транзакциям с указанной валютой.
    """
    for t in transactions:
        if t.get("currency") == currency:
            yield t
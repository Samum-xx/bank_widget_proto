def filter_by_currency(transactions, currency):
    valid_currencies = {"RUB", "USD", "EUR"}  # добавь сюда все допустимые валюты по ТЗ

    if currency not in valid_currencies:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    for t in transactions:
        if t.get("currency") == currency:
            yield t
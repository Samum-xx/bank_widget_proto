def filter_by_currency(transactions, currency):
    if currency not in {"RUB", "USD", "EUR"}:
        raise ValueError(f"Unsupported currency: {currency}")
    for t in transactions:
        if t.get("currency") == currency:
            yield t


def transaction_descriptions(transactions):
      for t in transactions:
        amount = t.get("amount", 0)
        currency = t.get("currency", "?")
        description = t.get("description", "без описания")
        yield f"{amount} {currency} — {description}"


def card_number_generator(start, stop):
    if start > stop:
        raise ValueError("start must be less than or equal to stop")
    for n in range(start, stop):
        yield n


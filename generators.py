from typing import Iterable, Dict, Any


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Iterable[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанной валюте.

    Args:
        transactions: Итерируемый объект (например, список) словарей с транзакциями.
        currency: Код валюты (RUB, USD, EUR).

    Yields:
        Словарь транзакции, если её валюта совпадает с запрашиваемой.

    Raises:
        ValueError: Если валюта не поддерживается.
    """
    valid_currencies = {"RUB", "USD", "EUR"}
    if currency not in valid_currencies:
        raise ValueError(f"Unsupported currency: {currency}")

    for t in transactions:
        if t.get("currency") == currency:
            yield t


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterable[str]:
    """
    Генерирует читаемые описания транзакций.

    Args:
        transactions: Итерируемый объект словарей с транзакциями.

    Yields:
        Строка в формате 'AMOUNT CURRENCY — DESCRIPTION'.
        Если поля нет, используются значения по умолчанию.
    """
    for t in transactions:
        amount = t.get("amount", 0)
        currency = t.get("currency", "?")
        description = t.get("description", "без описания")
        yield f"{amount} {currency} — {description}"


def card_number_generator(start: int, stop: int) -> Iterable[int]:
    """
    Генератор номеров карт в заданном диапазоне.

    Args:
        start: Начальное значение (включительно).
        stop: Конечное значение (не включительно), аналогично range().

    Yields:
        Целые числа от start до stop-1.

    Raises:
        ValueError: Если start больше stop.
    """
    if start > stop:
        raise ValueError("start must be less than or equal to stop")

    for n in range(start, stop):
        yield n
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("API_KEY")


def get_exchange_rate(currency: str) -> Optional[float]:
    """
    Запрашивает курс валюты к рублю через внешний API.
    Возвращает курс (float) или None при ошибке.
    """
    if not API_KEY:
        return None

    try:
        response = requests.get(
            API_URL,
            headers={"apikey": API_KEY},
            params={"base": currency, "symbols": "RUB"},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        rate = data.get("rates", {}).get("RUB")
        return float(rate) if rate is not None else None

    except (requests.RequestException, ValueError, KeyError):
        return None


def convert_to_rub(
    transaction: Dict[str, Any], rate_override: Optional[float] = None
) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: словарь с полями 'amount' и 'currency'.
        rate_override: опциональный курс для тестов (переопределяет реальный API).

    Returns:
        Сумма в рублях (float).
    """
    amount = transaction.get("amount", 0.0)
    currency = str(transaction.get("currency", "RUB")).upper()

    # Если валюта уже RUB — ничего не конвертируем
    if currency == "RUB":
        return float(amount)

    # Для валют, которые мы не поддерживаем в конвертации, возвращаем сумму как есть
    if currency not in ("USD", "EUR"):
        return float(amount)

    rate: Optional[float]

    # Если передан курс для теста — используем его
    if rate_override is not None:
        rate = rate_override
    else:
        # Иначе запрашиваем реальный курс
        rate = get_exchange_rate(currency)

        # Если курс не удалось получить, возвращаем исходную сумму
        if rate is None:
            return float(amount)

    # К этому моменту rate гарантированно не None, поэтому умножение безопасно
    return float(amount * rate)

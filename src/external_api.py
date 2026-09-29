import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Возвращает float:
      - Для RUB: amount как есть.
      - Для USD/EUR: конвертирует по курсу как из API.
      - При любой ошибке (нет ключа, сеть, неверный ответ): возвращает amount.
    """
    amount = transaction.get("amount", 0.0)
    currency = str(transaction.get("currency", "RUB")).upper()

    if currency == "RUB":
        return float(amount)

    if currency not in ("USD", "EUR"):
        return float(amount)

    if not API_KEY:
        return float(amount)

    try:
        response = requests.get(
            API_URL,
            headers={"apikey": API_KEY},
            params={"base": "USD", "symbols": currency},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        rate = rates.get(currency)

        if rate is None:
            return float(amount)

        return float(amount * rate)

    except (requests.RequestException, ValueError, KeyError):
        return float(amount)

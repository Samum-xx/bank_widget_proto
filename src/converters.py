import os
import requests
from typing import Optional

API_URL = "https://api.exchangerate.host/latest"

def convert_to_rub(amount: float, currency: str) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли.

    Args:
        amount (float): Сумма для конвертации.
        currency (str): Код валюты (например, 'USD', 'EUR').

    Returns:
        float: Сумма в рублях. При ошибке возвращается исходная сумма.
    """
    api_key = os.getenv("API_KEY")  # Берём ключ из .env
    params = {
        "base": currency,
        "symbols": "RUB",
    }
    if api_key:
        params["access_key"] = api_key  # Если твой API требует access_key

    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        rub_rate = rates.get("RUB")

        if rub_rate is None:
            return amount  # Нет курса — возвращаем как есть

        return round(amount * rub_rate, 2)

    except (requests.RequestException, ValueError, KeyError):
        # Любая ошибка сети, JSON или отсутствующего поля — возвращаем исходную сумму
        return amount
    
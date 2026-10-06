import re
from collections import Counter
from typing import Dict, List


class CurrencyFilter:
    @staticmethod
    def filter_by_currency(data, currency):
        return [item for item in data if isinstance(item, dict) and item.get("currency") == currency]


def count_operations_by_category(
        transactions: List[Dict],
        categories: List[str]
) -> Dict[str, int]:
    descriptions = [op.get("description", "") for op in transactions if isinstance(op, dict)]
    counter = Counter()
    for category in categories:
        count = sum(1 for desc in descriptions if category.lower() in desc.lower())
        counter[category] = count
    return dict(counter)


def process_bank_search(transactions: List[Dict], query: str) -> List[Dict]:
    if not query:
        return transactions

    # Компилируем паттерн, IGNORECASE — чтобы не зависеть от регистра
    pattern = re.compile(query, re.IGNORECASE)

    return [
        t for t in transactions
        if isinstance(t, dict) and pattern.search(t.get("description", ""))
    ]

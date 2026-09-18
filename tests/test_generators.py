import pytest
from generators import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture(scope="module")
def sample_transactions():
    return [
        {"amount": 100, "currency": "RUB", "description": "Оплата связи"},
        {"amount": 200, "currency": "USD", "description": "Amazon"},
        {"amount": 300, "currency": "RUB", "description": "Такси"},
        {"amount": 400, "currency": "EUR", "description": "Отель"},
        {"amount": 500, "currency": "USD"},
    ]

class TestFilterByCurrency:
    # ПАРАМЕТРИЗАЦИЯ: один тест покрывает все валюты
    @pytest.mark.parametrize(
        "currency, expected_count",
        [
            ("RUB", 2),
            ("USD", 2),
            ("EUR", 1),
        ],
    )
    def test_valid_currency_counts(self, sample_transactions, currency, expected_count):
        # Превращаем итератор в список только для проверки результата
        result = list(filter_by_currency(sample_transactions, currency=currency))
        assert len(result) == expected_count
        assert all(t["currency"] == currency for t in result)

    def test_invalid_currency_raises_error(self, sample_transactions):
        with pytest.raises(ValueError):
            list(filter_by_currency(sample_transactions, currency="JPY"))

    def test_empty_result_when_no_matches(self, sample_transactions):
        transactions_without_rub = [t for t in sample_transactions if t["currency"] != "RUB"]
        result = list(filter_by_currency(transactions_without_rub, currency="RUB"))
        assert result == []


class TestTransactionDescriptions:
    def test_normal_formatting(self, sample_transactions):
        result = list(transaction_descriptions(sample_transactions))
        assert len(result) == 5
        assert result[0] == "100 RUB — Оплата связи"
        assert result[-1] == "500 USD — без описания"

    def test_missing_fields_handling(self):
        transactions = [
            {"amount": 999},
            {},
        ]
        result = list(transaction_descriptions(transactions))
        assert result[0] == "999 ? — без описания"
        assert result[1] == "0 ? — без описания"


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "start, stop, expected_result",
        [
            (1000, 1005, [1000, 1001, 1002, 1003, 1004]),
            (5, 6, [5]),
            (10, 10, []),  # Пустой диапазон
        ],
    )
    def test_card_generator_ranges(self, start, stop, expected_result):
        result = list(card_number_generator(start, stop))
        assert result == expected_result

    def test_invalid_range_raises_error(self):
        with pytest.raises(ValueError):
            list(card_number_generator(1005, 1000))
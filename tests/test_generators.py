import pytest
from generators import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture(scope="module")
def sample_transactions():
    return [
        {"amount": 100, "currency": "RUB", "description": "Оплата связи"},
        {"amount": 200, "currency": "USD", "description": "Покупка на Amazon"},
        {"amount": 300, "currency": "RUB", "description": "Такси"},
        {"amount": 400, "currency": "EUR", "description": "Отель в Европе"},
        {"amount": 500, "currency": "USD"},
    ]

class TestFilterByCurrency:
    def test_valid_currency_rub(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, currency="RUB"))
        assert len(result) == 2
        assert all(t["currency"] == "RUB" for t in result)

    def test_valid_currency_usd(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, currency="USD"))
        assert len(result) == 2
        assert all(t["currency"] == "USD" for t in result)

    def test_valid_currency_eur(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, currency="EUR"))
        assert len(result) == 1
        # Берем первый элемент списка, потом ключ
        assert result[0]["amount"] == 400

    def test_invalid_currency_raises_error(self, sample_transactions):
        with pytest.raises(ValueError):
            list(filter_by_currency(sample_transactions, currency="JPY"))

    def test_empty_result_for_valid_currency(self, sample_transactions):
        transactions_without_rub = [t for t in sample_transactions if t["currency"] != "RUB"]
        result = list(filter_by_currency(transactions_without_rub, currency="RUB"))
        # Сравниваем с пустым списком
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
    def test_normal_range(self):
        result = list(card_number_generator(1000, 1005))
        assert result == [1000, 1001, 1002, 1003, 1004]

    def test_empty_range(self):
        result = list(card_number_generator(1000, 1000))
        assert result == []

    def test_invalid_range_raises_error(self):
        with pytest.raises(ValueError):
            list(card_number_generator(1005, 1000))

    def test_single_item_range(self):
        # Диапазон [5, 6) содержит только число 5
        result = list(card_number_generator(5, 6))
        assert result == [5]
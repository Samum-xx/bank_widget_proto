import pytest
from bank_widget_clean.widget import mask_account_card

class TestWidget:

    @pytest.mark.parametrize(
        "info, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 1234567890", "Счет **890"),
        ],
    )
    def test_valid_inputs(self, info, expected):
        assert mask_account_card(info) == expected

    @pytest.mark.parametrize(
        "info",
        [
            "",                 # Пустая строка
            "   ",              # Пробелы
            "Visa",             # Нет номера
            "7000792289606361", # Только номер, нет типа
            "Счет 123",        # Номер счета слишком короткий (но сначала проверим логику разбора)
            "Visa 123 abc",     # Лишние слова
            "Visa 1234567890123456 123456", # Слишком много чисел
        ],
    )
    def test_invalid_inputs_raise_error(self, info):
        # Согласно твоей реализации, функция выбрасывает ValueError для невалидных данных
        with pytest.raises(ValueError):
            mask_account_card(info)
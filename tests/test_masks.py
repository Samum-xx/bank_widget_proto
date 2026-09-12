import pytest
from bank_widget_clean.masks import get_mask_card_number, get_mask_account


class TestMasks:

    @pytest.mark.parametrize(
        "card, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),  # Валидная карта (16 цифр)
            ("1111222233334444", "1111 22** **** 4444"),  # Валидная карта
            ("", "Некорректный номер карты"),  # Пустая строка
            ("123", "Некорректный номер карты"),  # Слишком короткая
            ("abcdef", "Некорректный номер карты"),  # Не цифры
            ("123456789012345", "Некорректный номер карты"),  # 15 цифр (мало)
        ],
    )
    def test_get_mask_card_number(self, card, expected):
        assert get_mask_card_number(card) == expected

    @pytest.mark.parametrize(
        "account, expected",
        [
            ("73654108430135874305", "**4305"),  # Валидный счет
            ("1234567890", "**890"),  # Валидный счет (меньше 20 цифр)
            ("", "Некорректный номер счета"),  # Пустая строка
            ("12", "Некорректный номер счета"),  # Слишком короткая (<4)
            ("abcd", "Некорректный номер счета"),  # Не цифры
        ],
    )
    def test_get_mask_account(self, account, expected):
        assert get_mask_account(account) == expected
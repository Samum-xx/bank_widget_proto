import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card,expected", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("4111111111111111", "4111 11** **** 1111"),
])
def test_get_mask_card_number_valid(card, expected):
    assert get_mask_card_number(card) == expected


@pytest.mark.parametrize("invalid_input", [
    "",
    "1234",
    "7000a92289606361",
    "123",
])
def test_get_mask_card_number_invalid(invalid_input):
    assert get_mask_card_number(invalid_input) == "Некорректный номер карты"


@pytest.mark.parametrize("account,expected", [
    ("73654108430135874305", "**4305"),
    ("12345678901234567890", "**7890"),
])
def test_get_mask_account_valid(account, expected):
    assert get_mask_account(account) == expected


@pytest.mark.parametrize("invalid_account", [
    "",
    "12",
    "abc12345",
])
def test_get_mask_account_invalid(invalid_account):
    assert get_mask_account(invalid_account) == "Некорректный номер счета"

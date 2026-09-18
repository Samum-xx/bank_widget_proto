import pytest
from src.widget import mask_account_card, get_date


# --- Тесты mask_account_card ---

@pytest.mark.parametrize("info,expected_prefix", [
    ("Visa Platinum 7000792289606361", "Visa Platinum"),
    ("Mastercard 4111111111111111", "Mastercard"),
    ("Счет 73654108430135874305", "Счет"),
])
def test_mask_account_card_valid(info, expected_prefix):
    result = mask_account_card(info)
    assert result.startswith(expected_prefix)
    assert "****" in result or "**" in result


@pytest.mark.parametrize("bad_input", [
    "",
    "   ",
    "Visa",
    "Счет",
    "Visa 7000abc289606361",
])
def test_mask_account_card_raises_value_error(bad_input):
    with pytest.raises(ValueError):
        mask_account_card(bad_input)


def test_mask_account_card_case_insensitive_account():
    result = mask_account_card("счеТ 73654108430135874305")
    assert result.startswith("Счет")


def test_mask_account_card_unknown_type_masks_as_card():
    """Неизвестный тип карты маскируется как карта, без ошибки."""
    result = mask_account_card("UnknownType 1234567890123456")
    assert "****" in result
    assert result.startswith("UnknownType")


def test_mask_account_card_too_many_numbers():
    """Строка с двумя числовыми частями вызывает ValueError (строка 20)."""
    with pytest.raises(ValueError):
        mask_account_card("Visa 1234 7000792289606361")


# --- Тесты get_date ---

@pytest.mark.parametrize("iso_string,expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2000-01-01T00:00:00", "01.01.2000"),
])
def test_get_date_valid(iso_string, expected):
    assert get_date(iso_string) == expected


@pytest.mark.parametrize("bad_date", [
    "2024/03/11",
    "not-a-date",
    "",
])
def test_get_date_invalid(bad_date):
    with pytest.raises(ValueError):
        get_date(bad_date)

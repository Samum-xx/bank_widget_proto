import pytest

@pytest.fixture
def valid_card_info():
    """Валидная строка для карты: 'Тип Номер'"""
    return "Visa Platinum 7000792289606361"

@pytest.fixture
def valid_account_info():
    """Валидная строка для счета: 'Счет Номер'"""
    return "Счет 73654108430135874305"
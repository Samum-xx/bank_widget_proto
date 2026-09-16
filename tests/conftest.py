import pytest

@pytest.fixture
def sample_transactions():
    return [
        {"currency": "RUB", "amount": 100},
        {"currency": "USD", "amount": 200},
        {"currency": "EUR", "amount": 300},
    ]
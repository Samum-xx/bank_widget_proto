import pytest
from src.filters import process_bank_search
from src.filters import count_operations_by_category


@pytest.fixture
def sample_data():
    return [
        {"description": "Перевод организации", "state": "EXECUTED"},
        {"description": "Перевод с карты на карту", "state": "EXECUTED"},
        {"description": "Открытие вклада", "state": "EXECUTED"},
        {"description": "Оплата услуг", "status": "CANCELED"},
    ]


def test_count_operations_by_category(sample_data):
    transactions = sample_data
    categories = ["перевод", "оплата"]
    result = count_operations_by_category(transactions, categories)

    assert result["перевод"] == 2
    # "оплата" встречается 1 раз (в "Оплата услуг")
    assert result["оплата"] == 1


def test_count_operations_by_category_no_matches():
    transactions = [{"description": "Снятие наличных"}]
    categories = ["перевод", "оплата"]
    result = count_operations_by_category(transactions, categories)
    assert result == {"перевод": 0, "оплата": 0}


def test_count_operations_by_category_empty():
    result = count_operations_by_category([], ["перевод"])
    assert result == {"перевод": 0}

def test_process_bank_search_regex_alternation():
    transactions = [
        {"description": "Оплата картой"},
        {"description": "Перевод на счёт"},
        {"description": "Списание комиссии"},
    ]
    result = process_bank_search(transactions, r"оплата|перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Оплата картой"
    assert result[1]["description"] == "Перевод на счёт"

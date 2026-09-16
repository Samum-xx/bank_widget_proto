from bank_widget_clean.dates import get_date

def test_get_date_iso_format():
    assert get_date("Оплата от 2024-05-10") == "2024-05-10"

def test_get_date_dot_format():
    assert get_date("Дата: 10.05.2024") == "2024-05-10"
    assert get_date("1.1.2024") == "2024-01-01"

def test_get_date_no_date():
    assert get_date("") is None
    assert get_date("Текст без даты") is None

def test_get_date_invalid():
    # Невалидная дата должна вернуть None, а не падать с ошибкой
    assert get_date("Дата: 32.01.2024") is None
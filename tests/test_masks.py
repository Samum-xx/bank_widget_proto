from src.widget import mask_card_number


def test_mask_card_number_normal():
    # Обычный случай: номер без пробелов и дефисов
    assert mask_card_number("1234567890123456") == "XXXX XXXX XXXX 3456"

def test_mask_card_number_with_spaces():
    # Пробелы — функция должна их убрать
    assert mask_card_number("1111 2222 3333 4444") == "XXXX XXXX XXXX 4444"

def test_mask_card_number_with_dashes():
    # Дефисы — тоже должны исчезнуть
    assert mask_card_number("1234-5678-9012-3456") == "XXXX XXXX XXXX 3456"

def test_mask_card_number_too_short():
    # Слишком короткий номер — должна быть ошибка
    try:
        mask_card_number("12345")
        assert False, "Ожидалась ошибка, но её не было"
    except ValueError:
        # Всё ок: ошибка действительно возникла
        pass

def test_mask_card_number_with_letters():
    # Буквы в номере — тоже ошибка
    try:
        mask_card_number("1234ABCD56789012")
        assert False, "Ожидалась ошибка, но её не было"
    except ValueError:
        pass


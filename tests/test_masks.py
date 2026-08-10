from src.masks import get_mask_card_number, get_mask_account


def run_tests():
    print("\n--- Запуск ручных тестов ---")

    # Тест карты: формат XXXX XX** **** XXXX
    result_card = get_mask_card_number("7000792289606361")
    expected_card = "7000 79** **** 6361"
    assert result_card == expected_card, f"Карта: ожидалось {expected_card}, получено {result_card}"
    print(f"✅ Тест карты пройден: {result_card}")

    # Тест счёта: формат **XXXX
    result_account = get_mask_account("73654108430135874305")
    expected_account = "**4305"
    assert result_account == expected_account, f"Счёт: ожидалось {expected_account}, получено {result_account}"
    print(f"✅ Тест счёта пройден: {result_account}")

    print("--- Все тесты пройдены ---\n")


if __name__ == "__main__":
    run_tests()
def test_get_mask_card_number_invalid_length():
    from src.masks import get_mask_card_number
    try:
        get_mask_card_number("12345")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass


def test_get_mask_account_invalid_input():
    from src.masks import get_mask_account
    try:
        get_mask_account("abcd")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        pass
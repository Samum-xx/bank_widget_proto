from src.masks import get_mask_card_number

def test_get_mask_card_number_standard():
    assert get_mask_card_number("1234567890123456") == "123456******3456"

def test_get_mask_card_number_with_spaces():
    assert get_mask_card_number("1111 2222 3333 4444") == "111122******3344"

def test_get_mask_card_number_with_dashes():
    assert get_mask_card_number("1234-5678-9012-3456") == "123456******1234"

def test_short_card_raises():
    try:
        get_mask_card_number("12345")
        assert False, "Expected ValueError"
    except ValueError:
        pass
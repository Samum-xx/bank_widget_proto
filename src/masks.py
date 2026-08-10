def get_mask_card_number(card_number: str) -> str:
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("card_number должен быть строкой из 16 цифр")

    first_six = card_number[:6]
    last_four = card_number[-4:]

    block1 = first_six[:4]
    block2 = first_six[4:] + "**"
    block3 = "****"
    block4 = last_four

    return f"{block1} {block2} {block3} {block4}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.
    Формат вывода: **XXXX (видны только последние 4 цифры).
    """
    if not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("account_number должен содержать не менее 4 цифр")

    last_four = account_number[-4:]
    return f"**{last_four}"

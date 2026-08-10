def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты: оставляет первые 6 и последние 4 цифры,
    остальное заменяет на '*'.

    Примеры:
        '1234567890123456' -> '123456******3456'
        '1111 2222 3333 4444' -> '111122******3344'
        '1234-5678-9012-3456' -> '123456******1234'
    """
    clean_number = card_number.replace(" ", "").replace("-", "")

    if len(clean_number) < 10:
        raise ValueError("Card number is too short")

    prefix = clean_number[:6]
    suffix = clean_number[-4:]
    masked_middle = "*" * (len(clean_number) - 10)

    return f"{prefix}{masked_middle}{suffix}"

def get_mask_card_number(card_number: str) -> str:
    if len(card_number) < 10:
        return card_number  # или обработка ошибки, если номер слишком короткий
    return card_number[:6] + '*' * (len(card_number) - 10) + card_number[-4:]
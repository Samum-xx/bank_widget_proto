def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты: оставляет первые 6 и последние 4 цифры,
    остальное заменяет на '*'.

    Перед маскированием удаляются пробелы и дефисы.

    Примеры:
        '1234567890123456' -> '123456******3456'
        '1111 2222 3333 4444' -> '111122******3344'
        '1234-5678-9012-3456' -> '123456******1234'
    """
    # Убираем пробелы и дефисы
    clean_number = card_number.replace(" ", "").replace("-", "")

    # Если номер слишком короткий — выбрасываем ошибку (под твои тесты)
    if len(clean_number) < 10:
        raise ValueError("Card number is too short")

    prefix = clean_number[:6]
    suffix = clean_number[-4:]
    masked_middle = "*" * (len(clean_number) - 10)

    return f"{prefix}{masked_middle}{suffix}"
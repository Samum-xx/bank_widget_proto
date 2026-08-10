def mask_account_card(info: str) -> str:
    parts = info.rsplit(" ", 1)
    if len(parts) != 2:
        return info

    prefix, number_raw = parts

    if prefix.lower() == "счет":
        clean_number = "".join(c for c in number_raw if c.isdigit())
        if len(clean_number) <= 4:
            masked_number = clean_number
        else:
            masked_number = "*" * (len(clean_number) - 4) + clean_number[-4:]
        return f"{prefix} {masked_number}"

    # Для карт: сначала получаем маску через существующую функцию
    try:
        masked_card = get_mask_card_number(number_raw)
        # Теперь добавляем пробелы: 4 цифры, пробел, 4 звёздочки, пробел, 4 звёздочки, пробел, 4 цифры
        # Предполагаем, что masked_card — это строка из 16 символов после очистки
        if len(masked_card) == 16:
            formatted_card = f"{masked_card[:4]} {masked_card[4:8]} {masked_card[8:12]} {masked_card[12:]}"
            return f"{prefix} {formatted_card}"
        return f"{prefix} {masked_card}"
    except ValueError:
        return f"{prefix} {number_raw}"
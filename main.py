from src.widget import mask_account_card, get_date, get_last_successful_operations, format_operation_for_display

if __name__ == "__main__":
    print("--- Проверка маскирования ---")
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))

    print("\n--- Проверка даты ---")
    print(get_date("2024-03-11T02:26:18.671407"))

    print("\n--- Проверка виджета (последние успешные операции) ---")
    operations = [
        {"id": 1, "amount": 1200.5, "currency": "RUB", "status": "SUCCESS", "timestamp": "2024-08-10T10:00:00Z"},
        {"id": 2, "amount": 500.0, "currency": "RUB", "status": "FAILED", "timestamp": "2024-08-09T09:00:00Z"},
        {"id": 3, "amount": 3000.0, "currency": "RUB", "status": "SUCCESS", "timestamp": "2024-08-11T11:00:00Z"},
    ]
    last_ops = get_last_successful_operations(operations, limit=2)
    for op in last_ops:
        print(format_operation_for_display(op))
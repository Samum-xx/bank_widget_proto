import os
import sys

# --- Блок настройки путей (делает код рабочим везде: в PyCharm, в Docker, на сервере) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)
# ------------------------------------------------------------------------------------

# Теперь импортируем функцию просто из widget (без приставки src)
from widget import prepare_operations_widget_data

if __name__ == "__main__":
    # Тестовые данные для проверки логики
    operations = [
        {
            "id": 1,
            "status": "success",
            "card_number": "1234 5678 9012 3456",
            "amount": 1500,
            "currency": "RUB",
            "description": "Оплата в магазине",
            "created_at": "2024-10-05"
        },
        {
            "id": 2,
            "status": "failed",  # Эта операция должна исчезнуть из результата (фильтр по статусу)
            "card_number": "1111 2222 3333 4444",
            "amount": 500,
            "currency": "RUB",
            "description": "Ошибка платежа",
            "created_at": "2024-10-04"
        },
        {
            "id": 3,
            "status": "success",
            "card_number": "9999-8888-7777-6666",
            "amount": 3000,
            "currency": "USD",
            "description": "Перевод другу",
            "created_at": "2024-10-06"
        },
    ]

    # Вызываем функцию подготовки данных для виджета
    result = prepare_operations_widget_data(operations, limit=5)

    # Выводим результат в консоль
    print("Результат для виджета:")
    for op in result:
        print(op)
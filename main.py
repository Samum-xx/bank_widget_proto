from src.readers import read_json_file, read_csv_transactions, read_excel_transactions
from src.filters import process_bank_search
from datetime import datetime


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    data = []

    if choice == "1":
        data = read_json_file("operations.json")
    elif choice == "2":
        data = read_csv_transactions("operations.csv")
    elif choice == "3":
        data = read_excel_transactions("operations.xlsx")
    else:
        print("Неверный пункт меню.")
        return

    status = input("Введите статус (EXECUTED, CANCELED, PENDING): ").strip().upper()
    if status:
        data = [t for t in data if isinstance(t, dict) and t.get("state") == status]
        print(f"Операции отфильтрованы по статусу \"{status}\"")

    # Сортировка по дате
    sort_choice = input("Выполнить сортировку по дате? (да/нет): ").strip().lower()
    if sort_choice == "да":
        order = input("Порядок сортировки (по убыванию/по возрастанию): ").strip().lower()
        reverse = order == "по убыванию"

        def parse_date(op):
            if not isinstance(op, dict):
                return None
            d = op.get("date")
            if d:
                try:
                    return datetime.strptime(d, "%Y-%m-%d")
                except ValueError:
                    pass
            return None

        data.sort(key=parse_date, reverse=reverse)
        print(f"Операции отсортированы: {'по убыванию' if reverse else 'по возрастанию'}")

    search_choice = input("Выполнить поиск по описанию? (да/нет): ").strip().lower()
    if search_choice == "да":
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            data = process_bank_search(data, search_word)
            print(f"Выполнен поиск по описанию: \"{search_word}\"")

    if not data:
        print("Операций не найдено.")
    else:
        for op in data:
            if not isinstance(op, dict):
                continue
            description = op.get("description", "Без описания")
            date_str = op.get("date", "Нет даты")
            amount = op.get("amount", 0)
            currency = op.get("currency", "?")
            print(f"[{date_str}] {description} — {amount} {currency}")

    print(f"Итого отобрано операций: {len(data)}")

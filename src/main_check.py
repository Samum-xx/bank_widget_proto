from src.masks.masks import get_mask_card_number
from src.utils.utils import read_json_file
import os
import logging

print("Запуск проверки логирования...")

# 1. Проверяем маскирование (создаст masks.log)
masked = get_mask_card_number("1234567890123456")
print(f"Маска карты: {masked}")

# 2. Проверяем чтение JSON (создаст utils.log)
test_path = "temp_test.json"
with open(test_path, "w", encoding="utf-8") as f:
    f.write('{"test": "data"}')

data = read_json_file(test_path)
print(f"Данные из JSON: {data}")

os.remove(test_path)  # убираем временный файл

print("Проверка завершена. Загляни в папку logs")

logging.shutdown()

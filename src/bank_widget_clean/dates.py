import re
from datetime import datetime

def get_date(text: str):
    if not text or not isinstance(text, str):
        return None

    # 1. Ищем ISO формат (приоритет, так как однозначен): YYYY-MM-DD
    iso_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", text)
    if iso_match:
        y, m, d = iso_match.groups()
        try:
            datetime(int(y), int(m), int(d))
            return f"{y}-{m}-{d}"
        except ValueError:
            pass  # Невалидная дата (напр. 2024-02-30), идем дальше

    # 2. Ищем форматы с разделителями: DD.MM.YYYY или DD/MM/YYYY
    dot_slash_match = re.search(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b", text)
    if dot_slash_match:
        d, m, y = dot_slash_match.groups()
        try:
            # Проверка на реальную дату (отсекает 32.01.2024)
            datetime(int(y), int(m), int(d))
            return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
        except ValueError:
            pass

    return None
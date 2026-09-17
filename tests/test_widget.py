from src.widget import prepare_operations_widget_data


def test_prepare_operations_filters_only_success():
    ops = [
        {"id": 1, "status": "success", "card_number": "1111222233334444", "amount": 100, "created_at": "2025-01-02"},
        {"id": 2, "status": "failed", "card_number": "2222333344445555", "amount": 200, "created_at": "2025-01-03"},
        {"id": 3, "status": "success", "card_number": "3333444455556666", "amount": 300, "created_at": "2025-01-01"},
    ]
    result = prepare_operations_widget_data(ops, limit=5)
    # Должны остаться только успешные
    assert len(result) == 2
    assert all(op["status"] != "failed" for op in ops)  # тут мы не проверяем статус в result, потому что его там нет — это ок
    ids = [op["id"] for op in result]
    assert 2 not in ids  # failed операция не попала

def test_prepare_operations_sorts_new_first():
    ops = [
        {"id": 1, "status": "success", "card_number": "1111222233334444", "amount": 100, "created_at": "2025-01-01"},
        {"id": 2, "status": "success", "card_number": "2222333344445555", "amount": 200, "created_at": "2025-01-03"},
        {"id": 3, "status": "success", "card_number": "3333444455556666", "amount": 300, "created_at": "2025-01-02"},
    ]
    result = prepare_operations_widget_data(ops, limit=5)
    # IDs должны идти по убыванию даты: сначала 2 (03), потом 3 (02), потом 1 (01)
    assert [op["id"] for op in result] == [2, 3, 1]

def test_prepare_operations_limits_count():
    ops = [
        {"id": i, "status": "success", "card_number": "1111222233334444", "amount": i*10, "created_at": f"2025-01-{i:02d}"}
        for i in range(1, 11)  # 10 операций
    ]
    result = prepare_operations_widget_data(ops, limit=3)
    # Должно быть ровно 3
    assert len(result) == 3

def test_prepare_operations_masks_cards():
    ops = [
        {
            "id": 1,
            "status": "success",
            "card_number": "1234567890123456",
            "amount": 100,
            "created_at": "2025-01-02"
        }
    ]
    result = prepare_operations_widget_data(ops)
    assert result[0]["card_masked"] == "XXXX XXXX XXXX 3456"


import json
import pytest
from src.utils import read_json_file

def test_read_json_file_valid_list(tmp_path):
    data = [
        {"amount": 100.0, "currency": "RUB"},
        {"amount": 50.0, "currency": "USD"},
    ]
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == data

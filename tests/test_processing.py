import pytest

from src.processing import filter_by_state, sort_by_date
# --- Фикстуры ---

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2024-02-05T12:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-20T08:15:00"},
        {"id": 4, "state": "CANCELED", "date": "2024-03-01T18:45:00"},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-01T18:45:00"},
    ]


@pytest.fixture
def empty_data():
    return []


# --- Тесты filter_by_state ---

@pytest.mark.parametrize("state,expected_count", [
    ("EXECUTED", 3),
    ("PENDING", 1),
    ("CANCELED", 1),
    ("NONEXISTENT", 0),
])
def test_filter_by_state(sample_data, state, expected_count):
    filtered = filter_by_state(sample_data, state)
    assert len(filtered) == expected_count
    for item in filtered:
        assert item["state"] == state


def test_filter_by_state_default(sample_data):
    """Проверка значения по умолчанию — 'EXECUTED'."""
    filtered = filter_by_state(sample_data)
    assert len(filtered) == 3
    for item in filtered:
        assert item["state"] == "EXECUTED"


def test_filter_by_state_empty_list(empty_data):
    assert filter_by_state(empty_data, "EXECUTED") == []


def test_filter_by_state_no_match(sample_data):
    assert filter_by_state(sample_data, "ARCHIVED") == []


# --- Тесты sort_by_date ---

def test_sort_by_date_descending(sample_data):
    sorted_list = sort_by_date(sample_data, reverse=True)
    dates = [item["date"] for item in sorted_list]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_data):
    sorted_list = sort_by_date(sample_data, reverse=False)
    dates = [item["date"] for item in sorted_list]
    assert dates == sorted(dates)


def test_sort_by_date_same_dates(sample_data):
    """Проверка, что элементы с одинаковыми датами не теряются."""
    sorted_list = sort_by_date(sample_data, reverse=True)
    ids = [item["id"] for item in sorted_list]
    assert 3 in ids and 5 in ids  # оба элемента с датой 2024-03-01


def test_sort_by_date_default_is_descending(sample_data):
    """По умолчанию reverse=True — новые сначала."""
    sorted_list = sort_by_date(sample_data)
    assert sorted_list[0]["date"] == "2024-03-20T08:15:00"


def test_sort_by_date_empty_list(empty_data):
    assert sort_by_date(empty_data) == []


@pytest.mark.parametrize("reverse,first_date", [
    (True, "2024-03-20T08:15:00"),    # по убыванию — самая свежая
    (False, "2024-01-10T10:00:00"),   # по возрастанию — самая старая
])
def test_sort_by_date_first_element(sample_data, reverse, first_date):
    sorted_list = sort_by_date(sample_data, reverse=reverse)
    assert sorted_list[0]["date"] == first_date
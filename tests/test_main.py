import pytest
from main import main


def test_main_basic_flow(monkeypatch, capsys):
    # 1: JSON, EXECUTED, нет (сортировка), нет (RUB), нет (поиск)
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() != ""


def test_main_invalid_menu_choice(monkeypatch, capsys):
    inputs = iter(["999", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "Неверный пункт меню." in captured.out


def test_main_search_by_description(monkeypatch, capsys):
    # 1: JSON, EXECUTED, нет (сортировка), нет (RUB), да (поиск), "Оплата"
    inputs = iter(["1", "EXECUTED", "нет", "нет", "да", "Оплата"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "Оплата в магазине" in captured.out


def test_main_filter_by_date(monkeypatch, capsys):
    # 1: JSON, EXECUTED, да (сортировка), по убыванию (порядок), нет (RUB), нет (поиск)
    inputs = iter(["1", "EXECUTED", "да", "по убыванию", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))

    main()

    captured = capsys.readouterr()
    assert any(date in captured.out for date in ["2024-10-05", "2024-09-01"])

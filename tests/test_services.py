from src.services import *
from src.services import analyze_cashback_categories, investment_bank


SAMPLE_TRANSACTIONS = [
    {"Дата": "2023-05-15", "Сумма": 1000, "Категория": "Еда", "Описание": "Покупка в Пятерочке"},
    {"Дата": "2023-05-20", "Сумма": 5000, "Категория": "Техника", "Описание": "Покупка ноутбука"},
    {"Дата": "2023-06-01", "Сумма": 1712, "Категория": "Супермаркет", "Описание": "Я МТС +7 921 112233"},
    {"Дата": "2023-06-02", "Сумма": 2000, "Категория": "Переводы", "Описание": "Валерий А."},
]


def test_analyze_cashback_categories() -> None:
    result = analyze_cashback_categories(SAMPLE_TRANSACTIONS, 2023, 5)
    assert result == {"Еда": 50.0, "Техника": 250.0}  # 5% от сумм


def test_investment_bank() -> None:
    result = investment_bank("2023-06", SAMPLE_TRANSACTIONS, 50)
    assert result == (1750 - 1712)  # 1712 → 1750 (38 руб.)


def test_simple_search() -> None:
    result = simple_search(SAMPLE_TRANSACTIONS, "пятерочке")
    assert len(result) == 1
    assert result[0]["Сумма"] == 1000


def test_find_phone_transactions() -> None:
    result = find_phone_transactions(SAMPLE_TRANSACTIONS)
    assert len(result) == 1
    assert "+7 921" in result[0]["Описание"]


def test_find_person_transfers() -> None:
    result = find_person_transfers(SAMPLE_TRANSACTIONS)
    assert len(result) == 1
    assert "Валерий А." in result[0]["Описание"]

import pytest
from src.reports import *


@pytest.fixture
def sample_transactions():
    data = {
        "Date": pd.date_range(start="2023-01-01", end="2023-07-31", freq="D"),
        "Amount": [100 + i % 30 for i in range(212)],  # Имитация данных
        "Category": ["Food" if i % 3 else "Transport" for i in range(212)],
    }
    return pd.DataFrame(data)


def test_category_spending_report(sample_transactions):
    report = category_spending_report(sample_transactions, "Food", "2023-07-15")
    assert "Food" in report["category"]
    assert len(report["monthly_totals"]) == 3


def test_weekday_spending_report(sample_transactions):
    report = weekday_spending_report(sample_transactions)
    assert len(report["average_by_weekday"]) == 7
    assert "Monday" in report["average_by_weekday"]


def test_work_weekend_spending_report(sample_transactions):
    report = work_weekend_spending_report(sample_transactions)
    assert report["work_day_avg"] > 0
    assert report["weekend_avg"] > 0
    assert 0 <= report["ratio"] <= 2

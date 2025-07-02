import pytest
from src.views import *


@pytest.fixture
def sample_transactions(tmp_path):
    data = {
        "Date": ["2023-05-01", "2023-05-15", "2023-05-20", "2023-06-01"],
        "Card": ["1234567890123456", "1234567890123456", "9876543210987654", "1234567890123456"],
        "Amount": [1000, -5000, -3000, 2000],
        "Category": ["Income", "Food", "Transport", "Transfer"],
        "Description": ["Salary", "Groceries", "Taxi", "To friend"],
    }
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def test_get_time_greeting() -> None:
    assert get_time_greeting(datetime(2023, 1, 1, 8)) == "Доброе утро"
    assert get_time_greeting(datetime(2023, 1, 1, 14)) == "Добрый день"
    assert get_time_greeting(datetime(2023, 1, 1, 20)) == "Добрый вечер"
    assert get_time_greeting(datetime(2023, 1, 1, 2)) == "Доброй ночи"


def test_generate_home_page_data(sample_transactions):
    data = generate_home_page_data("2023-05-25 12:00:00")
    assert "greeting" in data
    assert len(data["cards"]) == 2
    assert data["cards"][0]["card_last4"] == "3456"


def test_generate_events_page_data(sample_transactions):
    data = generate_events_page_data("2023-05-25")
    assert data["expenses"]["total"] == 8000
    assert "Food" in data["expenses"]["main_categories"]
    assert "Transport" in data["expenses"]["main_categories"]

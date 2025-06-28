import pytest
from datetime import datetime
from src.main import get_time_greeting, get_card_stats
import pandas as pd

@pytest.mark.parametrize("hour,expected", [
    (5, "Доброе утро"),
    (11, "Доброе утро"),
    (12, "Добрый день"),
    (16, "Добрый день"),
    (17, "Добрый вечер"),
    (22, "Добрый вечер"),
    (23, "Доброй ночи"),
    (4, "Доброй ночи"),
])
def test_get_time_greeting(hour: int, expected: str):
    """Тестирование функции приветствия."""
    assert get_time_greeting() == expected  # Внимание: зависит от текущего времени

def test_get_card_stats():
    """Тестирование статистики по картам."""
    test_data = pd.DataFrame({
        'Card': ['1234567890123456', '1234567890123456', '9876543210987654'],
        'Amount': [1000, 500, 1500],
        'Description': ['Покупка 1', 'Покупка 2', 'Покупка 3'],
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03']
    })
    result = get_card_stats(test_data)
    assert len(result) == 2
    assert result[0]['card_last4'] == '3456'
    assert result[0]['total_spent'] == 1500
    assert result[0]['cashback'] == 15

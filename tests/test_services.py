import pandas as pd
from src.services import analyze_transactions


def test_analyze_transactions():
    data = {
        "Date": ["2024-01-01", "2024-01-02"],
        "Amount": [100, 200],
        "Category": ["Food", "Transport"],
    }
    df = pd.DataFrame(data)
    result = analyze_transactions(df)
    assert result["total_spent"] == 300

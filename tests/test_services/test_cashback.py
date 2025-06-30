from src.services.cashback import get_cashback_categories
import pandas as pd


def test_cashback():
    df = pd.DataFrame({"Category": ["Food", "Tech"], "Amount": [100, 500]})
    cashback_rules = {"Tech": 0.05}  # 5% кешбэка для категории Tech
    result = get_cashback_categories(df, cashback_rules)
    assert result["Tech"] == 25  # 500 * 0.05 = 25
    assert result.get("Food", 0) == 0  # Для Food кешбэка нет

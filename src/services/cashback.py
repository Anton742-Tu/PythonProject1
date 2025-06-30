import pandas as pd


def get_cashback_categories(df: pd.DataFrame, cashback_rules: dict) -> dict:
    """Возвращает сумму кешбэка по категориям."""
    cashback = {}
    for category, rate in cashback_rules.items():
        category_sum = df[df["Category"] == category]["Amount"].sum()
        cashback[category] = category_sum * rate
    return cashback

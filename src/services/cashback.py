import pandas as pd


def get_cashback_categories(df: pd.DataFrame, cashback_rules: dict) -> dict:
    """Возвращает категории с повышенным кешбэком."""
    df["Cashback"] = df["Category"].map(cashback_rules).fillna(0)
    return df.groupby("Category")["Cashback"].sum().to_dict()

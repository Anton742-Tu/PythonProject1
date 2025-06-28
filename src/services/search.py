import pandas as pd


def search_by_phone(df: pd.DataFrame, phone: str) -> pd.DataFrame:
    """Ищет транзакции по номеру телефона."""
    return df[df["Description"].str.contains(phone, na=False)]

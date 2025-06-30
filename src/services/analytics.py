import pandas as pd


def filter_data_by_month(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    """Фильтрует данные с начала месяца по указанную дату."""
    date = pd.to_datetime(target_date, dayfirst=True)
    start_date = date.replace(day=1)
    return df[(df["Date"] >= start_date) & (df["Date"] <= date)]

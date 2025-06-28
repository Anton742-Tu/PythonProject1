import pandas as pd


def weekday_report(df: pd.DataFrame) -> dict:
    """Анализ трат по дням недели."""
    df["Weekday"] = df["Date"].dt.day_name()
    return df.groupby("Weekday")["Amount"].sum().to_dict()

import pandas as pd


def work_weekend_report(df: pd.DataFrame) -> dict:
    """Сравнение трат в рабочие vs выходные дни."""
    df["Is_Weekend"] = df["Date"].dt.weekday >= 5
    return df.groupby("Is_Weekend")["Amount"].sum().to_dict()

import json
import pandas as pd


def save_json(data: dict, output_path: str) -> None:
    """Сохраняет данные в JSON."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def save_excel_report(df: pd.DataFrame, output_path: str) -> None:
    """Генерирует Excel-отчет."""
    summary = df.groupby("Category").agg({"Amount": ["sum", "count"]})
    summary.to_excel(output_path)

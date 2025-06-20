import pandas as pd


def load_excel(file_path: str) -> pd.DataFrame:
    """Загружает Excel-файл в DataFrame."""
    return pd.read_excel(file_path)

def validate_data(df: pd.DataFrame) -> bool:
    """Проверяет, что DataFrame содержит нужные колонки."""
    required_columns = {"Date", "Amount", "Category"}
    return required_columns.issubset(df.columns)

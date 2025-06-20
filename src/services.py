from typing import Dict, Any
import pandas as pd


def analyze_transactions(df: pd.DataFrame) -> Dict[str, Any]:
    """Анализирует транзакции и возвращает статистику."""
    return {
        "total_spent": df["Amount"].sum(),
        "by_category": df.groupby("Category")["Amount"].sum().to_dict(),
        "monthly": df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().to_dict(),
    }

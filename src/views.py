from fastapi import APIRouter
from services.analytics import filter_data_by_month
from services.finance_api import get_currency_rates, get_stock_prices
from src.models import ReportResponse
import pandas as pd
import json

router = APIRouter()


@router.get("/report/{target_date}", response_model=ReportResponse)
async def generate_report(target_date: str):
    # Загрузка данных
    df = pd.read_excel("data/operations.xlsx")
    filtered_df = filter_data_by_month(df, target_date)

    # Анализ
    total_spent = filtered_df["Amount"].sum()
    by_category = filtered_df.groupby("Category")["Amount"].sum().to_dict()

    # Загрузка внешних данных
    with open("user_settings.json") as f:
        settings = json.load(f)
    currencies = get_currency_rates(settings["user_currencies"])
    stocks = get_stock_prices(settings["user_stocks"])

    return {
        "period": f"01.{target_date[3:]} - {target_date}",
        "total_spent": total_spent,
        "by_category": by_category,
        "currencies": currencies,
        "stocks": stocks,
    }

import json
import logging
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, Literal
from functools import lru_cache

logger = logging.getLogger(__name__)

# Загрузка пользовательских настроек
with open("user_settings.json") as f:
    USER_SETTINGS = json.load(f)


def get_time_greeting(current_time: datetime = None) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    time = current_time or datetime.now()
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


@lru_cache(maxsize=32)
def get_currency_rates() -> Dict[str, float]:
    """Получает текущие курсы валют"""
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=RUB", timeout=5)
        rates = response.json()["rates"]
        return {curr: rates[curr] for curr in USER_SETTINGS["user_currencies"]}
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        return {}


@lru_cache(maxsize=32)
def get_stock_prices() -> Dict[str, float]:
    """Получает цены акций"""
    try:
        prices = {}
        for stock in USER_SETTINGS["user_stocks"]:
            response = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}", timeout=5)
            data = response.json()
            prices[stock] = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return prices
    except Exception as e:
        logger.error(f"Stock API error: {e}")
        return {}


def filter_by_date_range(
    df: pd.DataFrame, target_date: str, date_range: Literal["W", "M", "Y", "ALL"] = "M"
) -> pd.DataFrame:
    """Фильтрует данные по указанному диапазону дат"""
    date = pd.to_datetime(target_date)
    if date_range == "W":
        start_date = date - pd.Timedelta(days=date.weekday())
    elif date_range == "M":
        start_date = date.replace(day=1)
    elif date_range == "Y":
        start_date = date.replace(month=1, day=1)
    elif date_range == "ALL":
        start_date = df["Date"].min()
    else:
        raise ValueError("Invalid date range")

    return df[(df["Date"] >= start_date) & (df["Date"] <= date)]


def generate_home_page_data(datetime_str: str) -> Dict:
    """Генерирует данные для главной страницы"""
    try:
        # Загрузка и подготовка данных
        df = pd.read_excel("data/transactions.xlsx")
        df["Date"] = pd.to_datetime(df["Date"])

        # Фильтрация данных за текущий месяц
        current_date = pd.to_datetime(datetime_str)
        start_date = current_date.replace(day=1)
        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= current_date)]

        # Обработка данных по картам
        cards_data = []
        for card in filtered_df["Card"].unique():
            card_df = filtered_df[filtered_df["Card"] == card]
            total_spent = card_df["Amount"].sum()

            cards_data.append(
                {
                    "card_last4": str(card)[-4:],
                    "total_spent": round(total_spent),
                    "cashback": round(total_spent / 100),
                    "top_transactions": (
                        card_df.nlargest(5, "Amount")[["Date", "Amount", "Category", "Description"]].to_dict("records")
                    ),
                }
            )

        # Формирование ответа
        return {
            "greeting": get_time_greeting(current_date),
            "cards": cards_data,
            "currencies": get_currency_rates(),
            "stocks": get_stock_prices(),
            "generated_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error generating home page data: {e}")
        return {"error": str(e)}


def generate_events_page_data(datetime_str: str, date_range: Literal["W", "M", "Y", "ALL"] = "M") -> Dict:
    """Генерирует данные для страницы событий"""
    try:
        # Загрузка и подготовка данных
        df = pd.read_excel("data/transactions.xlsx")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Amount"] = df["Amount"].round()

        # Фильтрация данных
        filtered_df = filter_by_date_range(df, datetime_str, date_range)

        # Расходы
        expenses_df = filtered_df[filtered_df["Amount"] < 0]
        expenses_total = -expenses_df["Amount"].sum()

        # Основные категории расходов
        top_expenses = expenses_df.groupby("Category")["Amount"].sum().abs().sort_values(ascending=False)
        main_expenses = top_expenses.head(7).to_dict()
        other_expenses = top_expenses[7:].sum()

        # Переводы и наличные
        transfers_cash = (
            expenses_df[expenses_df["Category"].isin(["Переводы", "Наличные"])]
            .groupby("Category")["Amount"]
            .sum()
            .abs()
            .sort_values(ascending=False)
            .to_dict()
        )

        # Поступления
        income_df = filtered_df[filtered_df["Amount"] > 0]
        income_total = income_df["Amount"].sum()
        top_income = income_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).to_dict()

        # Формирование ответа
        return {
            "expenses": {
                "total": round(expenses_total),
                "main_categories": {k: round(v) for k, v in main_expenses.items()},
                "other_categories": round(other_expenses),
                "transfers_cash": {k: round(v) for k, v in transfers_cash.items()},
            },
            "income": {"total": round(income_total), "categories": {k: round(v) for k, v in top_income.items()}},
            "currencies": get_currency_rates(),
            "stocks": get_stock_prices(),
            "period": {
                "start": filtered_df["Date"].min().strftime("%Y-%m-%d"),
                "end": filtered_df["Date"].max().strftime("%Y-%m-%d"),
            },
        }

    except Exception as e:
        logger.error(f"Error generating events page data: {e}")
        return {"error": str(e)}

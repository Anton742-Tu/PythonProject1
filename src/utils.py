import json
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Union
import pandas as pd
from functools import wraps
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


# 1. Функции для работы с данными
def load_transactions(file_path: Union[str, Path] = "data/transactions.xlsx") -> pd.DataFrame:
    """Загружает транзакции из Excel-файла"""
    try:
        df = pd.read_excel(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        raise


def save_to_json(data: Any, filename: str) -> None:
    """Сохраняет данные в JSON-файл"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")
        raise


# 2. Функции для работы с датами
def get_date_range(target_date: str, period: str = "M") -> tuple:
    """Возвращает диапазон дат для анализа"""
    date = pd.to_datetime(target_date)
    if period == "D":
        return date, date
    elif period == "W":
        return date - timedelta(days=date.weekday()), date
    elif period == "M":
        return date.replace(day=1), date
    elif period == "Y":
        return date.replace(month=1, day=1), date
    elif period == "ALL":
        return pd.Timestamp.min, date
    else:
        raise ValueError(f"Unknown period: {period}")


def filter_by_date(df: pd.DataFrame, start_date: Union[str, datetime], end_date: Union[str, datetime]) -> pd.DataFrame:
    """Фильтрует DataFrame по диапазону дат"""
    return df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]


# 3. Функции для работы с финансами
def calculate_cashback(amount: float, rate: float = 0.01) -> float:
    """Вычисляет кешбэк (по умолчанию 1%)"""
    return round(amount * rate, 2)


def round_to_limit(amount: float, limit: int = 50) -> float:
    """Округляет сумму до заданного предела"""
    return ((amount // limit) + 1) * limit if amount % limit != 0 else amount


# 4. Валидаторы и проверки
def validate_card_number(card_number: str) -> bool:
    """Проверяет валидность номера карты"""
    return bool(re.match(r"^\d{16}$", str(card_number)))


def validate_date(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    """Проверяет корректность даты"""
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


# 5. Декораторы
def log_execution(func):
    """Декоратор для логирования выполнения функций"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Successfully executed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise

    return wrapper


# 6. Функции для работы с API
@log_execution
def fetch_currency_rates(currencies: List[str]) -> Dict[str, float]:
    """Получает курсы валют через API"""
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=RUB", timeout=10)
        rates = response.json().get("rates", {})
        return {curr: rates.get(curr, 0) for curr in currencies}
    except Exception as e:
        logger.error(f"Currency API error: {e}")
        return {curr: 0 for curr in currencies}


@log_execution
def fetch_stock_prices(stocks: List[str]) -> Dict[str, float]:
    """Получает цены акций через API"""
    prices = {}
    for stock in stocks:
        try:
            response = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}", timeout=10)
            data = response.json()
            prices[stock] = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        except Exception as e:
            logger.error(f"Failed to fetch {stock} price: {e}")
            prices[stock] = 0
    return prices


# 7. Вспомогательные функции
def format_currency(amount: float) -> str:
    """Форматирует денежные суммы"""
    return f"{amount:,.2f} ₽"


def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты (XXXX XXXX XXXX 3456)"""
    return f"**** **** **** {str(card_number)[-4:]}" if card_number else ""


def setup_logging() -> None:
    return None


def load_config() -> None:
    return None

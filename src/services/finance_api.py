import requests
import os
from datetime import datetime
from typing import Dict, List


def get_currency_rates(currencies: List[str]) -> Dict[str, float]:
    """Возвращает курсы валют через API (например, exchangerate-api.com)."""
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/RUB"
    response = requests.get(url).json()
    return {curr: response["rates"].get(curr) for curr in currencies}


def get_stock_prices(stocks: List[str]) -> Dict[str, float]:
    """Возвращает цены акций через Yahoo Finance или Alpha Vantage."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    prices = {}
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        data = requests.get(url).json()
        prices[stock] = float(data["Global Quote"]["05. price"])
    return prices

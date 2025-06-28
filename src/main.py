import logging
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import requests
from fastapi import APIRouter

router = APIRouter()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_time_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_card_stats(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает статистику по картам."""
    card_stats = []
    for card in df['Card'].unique():
        card_df = df[df['Card'] == card]
        total_spent = card_df['Amount'].sum()
        cashback = total_spent // 100  # 1 рубль за каждые 100 рублей

        card_stats.append({
            "card_last4": card[-4:],
            "total_spent": total_spent,
            "cashback": cashback,
            "top_transactions": card_df.nlargest(5, 'Amount').to_dict('records')
        })
    return card_stats


def get_currency_rates(currencies: List[str]) -> Dict[str, float]:
    """Получает курсы валют через API."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        rates = response.json()['rates']
        return {curr: rates.get(curr, 0) for curr in currencies}
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return {}


def get_sp500_stocks(stocks: List[str]) -> Dict[str, float]:
    """Получает цены акций из S&P500."""
    try:
        api_key = "YOUR_API_KEY"  # Замените на реальный API ключ
        prices = {}
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            prices[stock] = float(data['Global Quote']['05. price'])
        return prices
    except Exception as e:
        logger.error(f"Ошибка получения данных об акциях: {e}")
        return {}


@router.get("/main/{datetime_str}", response_model=Dict[str, Any])
async def get_main_page(datetime_str: str) -> Dict[str, Any]:
    """Главная страница с аналитикой."""
    try:
        # Парсинг даты
        current_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        # Загрузка данных
        df = pd.read_excel("data/transactions.xlsx")
        df['Date'] = pd.to_datetime(df['Date'])

        # Фильтрация данных за текущий месяц
        start_date = current_datetime.replace(day=1)
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= current_datetime)]

        # Формирование ответа
        response = {
            "greeting": get_time_greeting(),
            "cards": get_card_stats(filtered_df),
            "currencies": get_currency_rates(["USD", "EUR", "GBP"]),
            "stocks": get_sp500_stocks(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
        }

        return response

    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {e}")
        return {"error": str(e)}

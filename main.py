import logging
from typing import Optional, Literal

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.reports import category_spending_report, weekday_spending_report
from src.services import (
    analyze_cashback_categories,
    investment_bank,
)
from src.utils import setup_logging, load_config


def main() -> None:
    setup_logging()
    load_config()


from src.views import generate_home_page_data, generate_events_page_data


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Transaction Analyzer API", description="API для анализа банковских транзакций", version="1.0.0")


@app.get("/api/home")
async def home_page(datetime: str):
    """Главная страница с аналитикой"""
    try:
        return generate_home_page_data(datetime)
    except Exception as e:
        logger.error(f"Home page error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events")
async def events_page(datetime: str, range: Optional[Literal["W", "M", "Y", "ALL"]] = "M"):
    """Страница событий с аналитикой по периодам"""
    try:
        return generate_events_page_data(datetime, range)
    except Exception as e:
        logger.error(f"Events page error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/services/cashback")
async def cashback_service(year: int, month: int):
    """Сервис анализа выгодных категорий кешбэка"""
    try:
        transactions = load_transactions()
        return analyze_cashback_categories(transactions, year, month)
    except Exception as e:
        logger.error(f"Cashback service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/services/investment")
async def investment_service(month: str, limit: int = 50):
    """Сервис инвесткопилки с округлением трат"""
    try:
        transactions = load_transactions()
        return {"investment": investment_bank(month, transactions, limit)}
    except Exception as e:
        logger.error(f"Investment service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reports/category")
async def category_report(category: str, date: Optional[str] = None):
    """Отчет по тратам в категории"""
    try:
        df = load_transactions_dataframe()
        return category_spending_report(df, category, date)
    except Exception as e:
        logger.error(f"Category report error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reports/weekdays")
async def weekdays_report(date: Optional[str] = None):
    """Отчет по тратам по дням недели"""
    try:
        df = load_transactions_dataframe()
        return weekday_spending_report(df, date)
    except Exception as e:
        logger.error(f"Weekdays report error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def load_transactions():
    """Загрузка транзакций (заглушка)"""
    # Реальная реализация должна загружать из БД/файла
    return []


def load_transactions_dataframe():
    """Загрузка транзакций в DataFrame (заглушка)"""
    # Реальная реализация должна загружать из БД/файла
    return pd.DataFrame()


@app.exception_handler(Exception)
async def global_exception_handler(exc):
    """Глобальный обработчик исключений"""
    logger.critical(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config="logging.conf")

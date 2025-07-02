import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional, Union

logger = logging.getLogger(__name__)


# Декоратор для сохранения отчетов
def report_to_file(filename: Optional[str] = None):
    """
    Декоратор для сохранения результатов отчета в файл.
    Если имя файла не указано, генерирует автоматическое.
    """

    def decorator(report_func: Callable):
        @wraps(report_func)
        def wrapper(*args, **kwargs):
            try:
                result = report_func(*args, **kwargs)

                # Генерация имени файла если не указано
                output_file = filename or (
                    f"report_{report_func.__name__}_" f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )

                # Сохранение в файл
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

                logger.info(f"Отчет сохранен в файл: {output_file}")
                return result

            except Exception as e:
                logger.error(f"Ошибка при генерации отчета {report_func.__name__}: {e}")
                raise

        return wrapper

    return decorator


# 1. Отчет по категории
@report_to_file()
def category_spending_report(df: pd.DataFrame, category: str, target_date: Optional[str] = None) -> dict:
    """
    Возвращает траты по категории за последние 3 месяца.
    Формат результата:
    {
        "category": "Еда",
        "period": "2023-05-01 - 2023-07-31",
        "monthly_totals": {
            "2023-05": 15000,
            "2023-06": 12000,
            "2023-07": 18000
        }
    }
    """
    try:
        date = pd.to_datetime(target_date) if target_date else datetime.now()
        end_date = date.replace(day=1)
        start_date = (end_date - timedelta(days=90)).replace(day=1)

        filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date) & (df["Category"] == category)]

        monthly = filtered.groupby(filtered["Date"].dt.to_period("M"))["Amount"].sum()

        return {
            "category": category,
            "period": f"{start_date.date()} - {end_date.date()}",
            "monthly_totals": {str(k): float(v) for k, v in monthly.items()},
        }
    except Exception as e:
        logger.error(f"Ошибка в category_spending_report: {e}")
        return {}


# 2. Отчет по дням недели
@report_to_file()
def weekday_spending_report(df: pd.DataFrame, target_date: Optional[str] = None) -> dict:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.
    Формат результата:
    {
        "period": "2023-05-01 - 2023-07-31",
        "average_by_weekday": {
            "Monday": 1500,
            "Tuesday": 2000,
            ...
        }
    }
    """
    try:
        date = pd.to_datetime(target_date) if target_date else datetime.now()
        end_date = date.replace(day=1)
        start_date = (end_date - timedelta(days=90)).replace(day=1)

        filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
        filtered["Weekday"] = filtered["Date"].dt.day_name()

        avg_spending = filtered.groupby("Weekday")["Amount"].mean()

        return {
            "period": f"{start_date.date()} - {end_date.date()}",
            "average_by_weekday": {k: float(v) for k, v in avg_spending.items()},
        }
    except Exception as e:
        logger.error(f"Ошибка в weekday_spending_report: {e}")
        return {}


# 3. Отчет рабочие/выходные дни
@report_to_file("work_weekend_report.json")
def work_weekend_spending_report(df: pd.DataFrame, target_date: Optional[str] = None) -> dict:
    """
    Возвращает сравнение трат в рабочие vs выходные дни.
    Формат результата:
    {
        "period": "2023-05-01 - 2023-07-31",
        "work_day_avg": 1500,
        "weekend_avg": 3000,
        "ratio": 0.5
    }
    """
    try:
        date = pd.to_datetime(target_date) if target_date else datetime.now()
        end_date = date.replace(day=1)
        start_date = (end_date - timedelta(days=90)).replace(day=1)

        filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
        filtered["IsWeekend"] = filtered["Date"].dt.weekday >= 5

        avg_spending = filtered.groupby("IsWeekend")["Amount"].mean()

        work_avg = float(avg_spending.get(False, 0))
        weekend_avg = float(avg_spending.get(True, 0))

        return {
            "period": f"{start_date.date()} - {end_date.date()}",
            "work_day_avg": work_avg,
            "weekend_avg": weekend_avg,
            "ratio": weekend_avg / work_avg if work_avg else 0,
        }
    except Exception as e:
        logger.error(f"Ошибка в work_weekend_spending_report: {e}")
        return {}

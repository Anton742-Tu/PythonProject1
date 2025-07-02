import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Any
from functools import reduce

logger = logging.getLogger(__name__)


# 1. Сервис повышенного кешбэка
def analyze_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодность категорий для кешбэка.
    Возвращает словарь {категория: сумма кешбэка}.
    """
    try:
        filtered = filter(
            lambda t: datetime.strptime(t["Дата"], "%Y-%m-%d").year == year
            and datetime.strptime(t["Дата"], "%Y-%m-%d").month == month,
            data,
        )

        grouped = reduce(lambda acc, t: {**acc, t["Категория"]: acc.get(t["Категория"], 0) + t["Сумма"]}, filtered, {})

        return {k: v * 0.05 for k, v in grouped.items()}  # 5% кешбэк

    except Exception as e:
        logger.error(f"Ошибка анализа кешбэка: {e}")
        return {}


# 2. Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки через округление.
    limit: шаг округления (10, 50, 100)
    """
    try:
        monthly_trans = filter(lambda t: t["Дата"].startswith(month), transactions)

        rounded_sum = sum(
            (amount // limit + 1) * limit if amount % limit != 0 else amount
            for t in monthly_trans
            if (amount := float(t["Сумма"])) > 0
        )

        actual_sum = sum(float(t["Сумма"]) for t in monthly_trans if float(t["Сумма"]) > 0)

        return rounded_sum - actual_sum

    except Exception as e:
        logger.error(f"Ошибка расчета инвесткопилки: {e}")
        return 0.0


# 3. Простой поиск
def simple_search(transactions: List[Dict[str, Any]], search_query: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по подстроке в описании или категории.
    """
    query = search_query.lower()
    return list(filter(lambda t: query in t["Описание"].lower() or query in t["Категория"].lower(), transactions))


# 4. Поиск по телефонным номерам
def find_phone_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ищет транзакции с номерами телефонов в описании.
    """
    phone_pattern = re.compile(r"\+7\s?\d{3}\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}")
    return list(filter(lambda t: bool(phone_pattern.search(t["Описание"])), transactions))


# 5. Поиск переводов физлицам
def find_person_transfers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ищет переводы физлицам (формат "Имя Ф.").
    """
    name_pattern = re.compile(r"[А-Я][а-я]+\s[А-Я]\.")
    return list(
        filter(lambda t: t["Категория"] == "Переводы" and bool(name_pattern.search(t["Описание"])), transactions)
    )


# Вспомогательная функция для тестирования
def to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)

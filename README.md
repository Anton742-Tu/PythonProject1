# КУРСОВАЯ РАБОТА
##  на тему: "Обслуживание клиентов банка"


### Структура модуля:

Загрузка и сохранение данных:
 - load_transactions() - загрузка из Excel
 - save_to_json() - сохранение отчетов

Работа с датами:
 - get_date_range() - вычисление периодов
 - filter_by_date() - фильтрация DataFrame

Финансовые расчеты:
 - calculate_cashback() - вычисление кешбэка
 - round_to_limit() - округление для инвесткопилки

Валидация данных:
 - validate_card_number() - проверка номера карты
 - validate_date() - проверка формата даты

Декораторы:
 - log_execution() - логирование выполнения функций

Работа с внешними API:
 - fetch_currency_rates() - получение курсов валют
 - fetch_stock_prices() - получение цен акций

Вспомогательные функции:
 - format_currency() - форматирование сумм
 - mask_card_number() - маскировка номеров карт
```
from utils import (
    load_transactions,
    get_date_range,
    calculate_cashback,
    fetch_currency_rates
)

# Загрузка данных
df = load_transactions()

# Получение диапазона дат
start, end = get_date_range("2023-05-20", "M")

# Фильтрация данных
filtered_df = filter_by_date(df, start, end)

# Финансовые расчеты
cashback = calculate_cashback(1000, 0.05)  # 50 руб

# Получение курсов валют
rates = fetch_currency_rates(["USD", "EUR"])
```
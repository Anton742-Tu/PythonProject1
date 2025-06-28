from fastapi import FastAPI
from zoneinfo._common import load_data

from reports.by_weekday import weekday_report

app = FastAPI()

@app.get("/report/weekday")
async def report_weekday():
    df = load_data()  # Загрузка из Excel
    return weekday_report(df)

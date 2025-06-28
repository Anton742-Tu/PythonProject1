from pydantic import BaseModel
from typing import Dict


class ReportResponse(BaseModel):
    period: str
    total_spent: float
    by_category: Dict[str, float]
    currencies: Dict[str, float]
    stocks: Dict[str, float]

from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from app.models.statistics.category import Category


class Statistics(BaseModel):
    total: Decimal = Field(..., ge=0)
    categories: List[Category]

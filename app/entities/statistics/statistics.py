from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List

from app.entities.statistics.category import Category


class Statistics(BaseModel):
    total: Decimal = Field(..., ge=0)
    categories: List[Category]

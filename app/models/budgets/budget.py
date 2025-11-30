from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class BudgetDto(BaseModel):
    type: str
    month: int
    year: int
    value: Decimal = Field(..., ge=0)

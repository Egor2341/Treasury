from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class Month(BaseModel):
    name: str
    year: int = Field(..., ge=2000, le=2025)



class Budgets(BaseModel):
    current_real: Decimal = Field(..., ge=0)
    prev_months_real: List[Month] = Field(..., min_length=12, max_length=12)
    current_theory: Decimal = Field(..., ge=0)
    prev_months_theory: List[Month] = Field(..., min_length=12, max_length=12)


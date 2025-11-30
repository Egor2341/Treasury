from decimal import Decimal

from pydantic import BaseModel, Field


class Expense(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="min = 1, max = 32")
    value: Decimal

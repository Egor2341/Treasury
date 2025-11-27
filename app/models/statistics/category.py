from decimal import Decimal

from pydantic import BaseModel, Field


class Category(BaseModel):
    title: str = Field(..., min_length=1, max_length=64, description="min = 1, max = 64")
    price: Decimal = Field(..., ge=0)
from decimal import Decimal

from pydantic import BaseModel, Field


class Stat(BaseModel):
    count: int
    value: Decimal = Field(..., ge=0)

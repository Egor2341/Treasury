from decimal import Decimal

from pydantic import BaseModel, Field


class Edit(BaseModel):
    name: str
    budget: Decimal = Field(..., ge=0)
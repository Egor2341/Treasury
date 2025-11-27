from decimal import Decimal

from pydantic import BaseModel, Field


class Search(BaseModel):
    total: Decimal = Field(..., ge=0)
from decimal import Decimal

from pydantic import BaseModel, Field


class SearchResultDto(BaseModel):
    value: Decimal = Field(..., ge=0)
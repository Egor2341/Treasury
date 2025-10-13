from pydantic import BaseModel, Field
from decimal import Decimal

class Search(BaseModel):
    total: Decimal = Field(..., ge=0)
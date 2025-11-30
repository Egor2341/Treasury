from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from models.statistics.item import ItemDto


class ListItems(BaseModel):
    total: Decimal = Field(..., ge=0)
    categories: List["ItemDto"]

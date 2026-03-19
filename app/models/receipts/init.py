from typing import List

from pydantic import BaseModel


class Init(BaseModel):
    receipts: List["Receipt"]
    count: int

from models.receipts.one import Receipt
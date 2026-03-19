from typing import List

from pydantic import BaseModel


class ListReceipts(BaseModel):
    receipts: List["Receipt"]

from models.receipts.one import Receipt
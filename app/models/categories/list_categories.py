from typing import List

from pydantic import BaseModel


class ListCategories(BaseModel):
    expenses: List[str]
    e_uuids: List[str]
    e_count: int
    incomes: List[str]
    i_uuids: List[str]
    i_count: int

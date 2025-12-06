from typing import List

from pydantic import BaseModel


class ListCategories(BaseModel):
    expenses: List["str"]
    incomes: List["str"]

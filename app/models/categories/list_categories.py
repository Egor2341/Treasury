from typing import List

from pydantic import BaseModel


class ListCategories(BaseModel):
    categories_expenses: List["str"]
    categories_incomes: List["str"]

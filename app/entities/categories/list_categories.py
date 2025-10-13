from typing import List

from pydantic import BaseModel

from app.entities.categories.category import Category


class ListCategories(BaseModel):
    categories_expenses: List[Category]
    categories_theory: List[Category]
from typing import List

from pydantic import BaseModel

from models.budgets.budget import BudgetDto


class SearchResultBudgets(BaseModel):
    budgets: List["BudgetDto"]

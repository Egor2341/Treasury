from typing import List

from pydantic import BaseModel

from models.budgets.budget import BudgetDto


class ListBudgets(BaseModel):
    budgets_expenses: List["BudgetDto"]
    budgets_incomes: List["BudgetDto"]

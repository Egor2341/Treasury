import datetime
import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.budget import Budget
from data.entities.category import Category
from data.entities.expense import Expense
from data.entities.user import User
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from models.budgets.budget import BudgetDto
from models.budgets.list_budgets import ListBudgets
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from models.statistics.item import ItemDto
from models.statistics.list_items import ListItems
from decimal import Decimal




async def get_budgets(session: AsyncSession, user_uuid: str) -> ListBudgets:
    query = (
        select(Budget)
        .where(Budget.user_uuid == user_uuid)
        .order_by(Budget.year.desc(), Budget.month.desc())
        .limit(6)
    )

    result = await session.execute(query)
    budgets = result.scalars().all()

    return ListBudgets(
        budgets_expenses=[BudgetDto(type="expense", month=bud.month, year=bud.year, value=bud.value)
                          for bud in budgets if bud.type == "expense"],
        budgets_incomes= [BudgetDto(type="incomes", month=bud.month, year=bud.year, value=bud.value)
                          for bud in budgets if bud.type == "income"]
    )

async def edit_budgets(session: AsyncSession, data: BudgetDto, user_uuid: uuid):

    await session.execute(
        update(Budget)
        .where(
            Budget.user_uuid == user_uuid,
            Budget.type == data.type,
            Budget.month == data.month,
            Budget.year == data.year
        )
        .values(value=data.value)
    )


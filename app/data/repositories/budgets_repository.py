import datetime
import uuid
from decimal import Decimal

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data.entities.budget import Budget
from data.entities.expense import Expense
from data.entities.incomes import Income
from models.budgets.budget import BudgetDto
from models.budgets.list_budgets import ListBudgets
from models.budgets.search_result import SearchResultBudgets


async def get_budgets(session: AsyncSession, user_uuid: str) -> ListBudgets:
    query = (
        select(Budget)
        .filter_by(user_uuid=user_uuid, year=datetime.datetime.now().year)
    )

    result = await session.execute(query)
    budgets = result.scalars().all()

    return ListBudgets(
        real=[BudgetDto(type=bud.type, month=bud.month, year=bud.year, value=bud.value)
              for bud in budgets if bud.type == "real"],
        theory=[BudgetDto(type=bud.type, month=bud.month, year=bud.year, value=bud.value)
                for bud in budgets if bud.type == "theory"]
    )


async def calculate_real(session: AsyncSession, user_uuid: uuid):
    query = select(Expense).filter_by(user_uuid=user_uuid)
    result = await session.execute(query)
    expenses = result.scalars().all()

    query = select(Income).filter_by(user_uuid=user_uuid)
    result = await session.execute(query)
    incomes = result.scalars().all()

    return sum([inc.value for inc in incomes], Decimal(0)) - sum([exp.value for exp in expenses], Decimal(0))


async def edit_budgets(session: AsyncSession, data: BudgetDto, user_uuid: uuid):
    if data.type == "real":
        data.value = await calculate_real(session, user_uuid)

    query = (
        select(Budget)
        .filter_by(user_uuid=user_uuid, type=data.type, month=data.month, year=data.year)
    )

    result = await session.execute(query)
    budget = result.first()

    if (budget):
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
    else:
        new_budget = Budget(user_uuid=user_uuid, type=data.type, month=data.month, year=data.year, value=data.value)

        session.add(new_budget)


async def search_budgets(session: AsyncSession, user_uuid: uuid, type: str, year: int):
    query = (
        select(Budget)
        .filter_by(user_uuid=user_uuid, year=year, type=type)
    )
    result = await session.execute(query)
    budgets = result.scalars().all()


    return SearchResultBudgets(
        budgets=[BudgetDto(type=type, month=bud.month, year=bud.year, value=bud.value)
                 for bud in budgets]
    )

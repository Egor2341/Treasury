import datetime
import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data.entities.category import Category
from data.entities.expense import Expense
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from models.statistics.item import ItemResponseDto
from models.statistics.list_items import ListItems
from decimal import Decimal

from models.statistics.search import SearchResultDto


async def add_expense(session: AsyncSession, data: ItemResponseDto, user_uuid: uuid):
    query = select(Category).filter_by(user_uuid=user_uuid, name=data.name)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if category is None:
        raise NoEntryError("The category does not exist")

    cur_date = datetime.datetime.now()
    query = select(Expense).filter_by(user_uuid=user_uuid, name=data.name)
    result = await session.execute(query)
    expense_from_db = result.scalar_one_or_none()
    if expense_from_db is None:
        new_expense = Expense(user_uuid=user_uuid, name=category.name, value=data.value,
                              month=cur_date.month, year=cur_date.year)

        session.add(new_expense)
    else:
        raise DuplicatedEntryError("This expense already exist")


async def get_expenses(session: AsyncSession, user_uuid: str) -> ListItems:
    query = select(Expense).filter_by(user_uuid=user_uuid)
    result = await session.execute(query)
    expenses = result.scalars().all()

    return ListItems(
        total=sum([exp.value for exp in expenses], Decimal(0)),
        items=[ItemResponseDto(name=exp.name, value=exp.value) for exp in expenses]
    )


async def edit_expense(session: AsyncSession, data: ItemResponseDto, user_uuid: uuid):
    await session.execute(
        update(Expense)
        .where(
            Expense.user_uuid == user_uuid,
            Expense.name == data.name
        )
        .values(value=data.value)
    )


async def delete_expense(session: AsyncSession, name: str, user_uuid: uuid):
    await session.execute(
        delete(Expense)
        .where(
            Expense.user_uuid == user_uuid,
            Expense.name == name,
        )
    )


async def search_expense(title: str,
                         year: int,
                         month: str,
                         user_uuid: uuid,
                         session: AsyncSession,
                         ):
    if (month == "Все"):
        query = select(Expense).filter_by(
            user_uuid=user_uuid,
            name=title,
            year=year,
        )
    else:
        query = select(Expense).filter_by(
            user_uuid=user_uuid,
            name=title,
            year=year,
            month=monthToInt(month)
        )
    result = await session.execute(query)
    expenses = result.scalars().all()

    return SearchResultDto(value=sum([exp.value for exp in expenses], Decimal(0)))


def monthToInt(month: str):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    months_dict = {month: i + 1 for i, month in enumerate(months)}
    return months_dict[month]

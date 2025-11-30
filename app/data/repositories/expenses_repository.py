import datetime
import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.category import Category
from data.entities.expense import Expense
from data.entities.user import User
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from models.statistics.item import ItemDto
from models.statistics.list_items import ListItems
from decimal import Decimal



async def add_expense(session: AsyncSession, data: ItemDto, user_uuid: uuid):
    query = select(Category).filter_by(user_uuid=user_uuid, name=data.name)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if category is None:
        raise NoEntryError("The category does not exist")

    cur_date = datetime.datetime.now()
    new_expense = Expense(user_uuid=user_uuid, name=category.name, value=data.value,
                          month=cur_date.month, year=cur_date.year)

    session.add(new_expense)


async def get_expenses(session: AsyncSession, user_uuid: str) -> ListItems:
    query = select(Expense).filter_by(user_uuid=user_uuid)
    result = await session.execute(query)
    expenses = result.scalars().all()

    return ListItems(
        total=sum([exp.value for exp in expenses], Decimal(0)),
        categories=[ItemDto(name=exp.name, value=exp.value) for exp in expenses]
    )


async def edit_expense(session: AsyncSession, data: ItemDto, user_uuid: uuid):

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

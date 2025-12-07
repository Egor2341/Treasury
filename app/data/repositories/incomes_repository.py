import datetime
import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.category import Category
from data.entities.expense import Expense
from data.entities.incomes import Income
from data.entities.user import User
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from models.statistics.item import ItemResponseDto
from models.statistics.list_items import ListItems
from decimal import Decimal

from models.statistics.search import SearchResultDto


async def add_income(session: AsyncSession, data: ItemResponseDto, user_uuid: uuid):
    query = select(Category).filter_by(user_uuid=user_uuid, name=data.name)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if category is None:
        raise NoEntryError("The category does not exist")

    cur_date = datetime.datetime.now()
    new_income = Income(user_uuid=user_uuid, name=category.name, value=data.value,
                          month=cur_date.month, year=cur_date.year)

    session.add(new_income)


async def get_incomes(session: AsyncSession, user_uuid: str) -> ListItems:
    query = select(Income).filter_by(user_uuid=user_uuid)
    result = await session.execute(query)
    incomes = result.scalars().all()

    return ListItems(
        total=sum([inc.value for inc in incomes], Decimal(0)),
        items=[ItemResponseDto(name=inc.name, value=inc.value) for inc in incomes]
    )


async def edit_income(session: AsyncSession, data: ItemResponseDto, user_uuid: uuid):

    await session.execute(
        update(Income)
        .where(
            Income.user_uuid == user_uuid,
            Income.name == data.name
        )
        .values(value=data.value)
    )


async def delete_income(session: AsyncSession, name: str, user_uuid: uuid):
    await session.execute(
        delete(Income)
        .where(
            Income.user_uuid == user_uuid,
            Income.name == name,
        )
    )

async def search_income(title: str,
                         year: int,
                         month: str,
                         user_uuid: uuid,
                         session: AsyncSession,
                         ):
    if (month == "Все"):
        query = select(Income).filter_by(
            user_uuid=user_uuid,
            name=title,
            year=year,
        )
    else:
        query = select(Income).filter_by(
            user_uuid=user_uuid,
            name=title,
            year=year,
            month=monthToInt(month)
        )
    result = await session.execute(query)
    incomes = result.scalars().all()

    return SearchResultDto(value=sum([inc.value for inc in incomes], Decimal(0)))


def monthToInt(month: str):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    months_dict = {month: i + 1 for i, month in enumerate(months)}
    return months_dict[month]

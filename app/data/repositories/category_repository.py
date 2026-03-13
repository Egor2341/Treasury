import uuid

from sqlalchemy import update, delete, select
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
from models.categories.list_categories import ListCategories
from models.categories.list_one_type_categories import ListOneTypeCategories

LIMIT = 5


async def add_category(session: AsyncSession, data: CategoryDto, user_uuid: uuid):
    query = select(User).options(selectinload(User.categories)).filter_by(uuid=user_uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    new_category = Category(name=data.name, type=data.type, user_uuid=user_uuid)

    if len([cat.name for cat in user.categories if cat.name == data.name]) > 0:
        raise DuplicatedEntryError("This category already exists")

    session.add(new_category)


async def get_categories(session: AsyncSession, user_uuid: str) -> ListCategories:
    query = select(User).options(selectinload(User.categories)).filter_by(uuid=user_uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    return ListCategories(
        expenses=[cat.name for cat in user.categories if cat.type == "expenses"],
        incomes=[cat.name for cat in user.categories if cat.type == "incomes"]
    )


async def update_category(session: AsyncSession, data: EditDto, user_uuid: uuid):
    if data.old_name == data.new_name:
        raise DuplicatedEntryError("Old name and new name are the same")
    await session.execute(
        update(Category)
        .where(
            Category.user_uuid == user_uuid,
            Category.name == data.old_name,
            Category.type == data.type
        )
        .values(name=data.new_name)
    )


async def get_all_categories(session: AsyncSession,
                             user_uuid: str,
                             page_e: int,
                             page_i: int,
                             order_e: bool,
                             order_i: bool
                             ) -> ListCategories:
    expenses = await get_one_type_categories(session, user_uuid, "e", page_e, order_e)
    incomes = await get_one_type_categories(session, user_uuid, "i", page_i, order_i)

    return ListCategories(
        expenses=expenses.categories,
        incomes=incomes.categories
    )


async def get_one_type_categories(session: AsyncSession,
                                  user_uuid: str,
                                  type: str,
                                  page,
                                  order
                                  ) -> ListOneTypeCategories:
    type = Expense if type == "e" else Income
    stmt = select(type)
    stmt = stmt.order_by(type.name) if order else stmt.order_by(type.name.desc())
    stmt = stmt.where(type.user_uuid == user_uuid).limit(LIMIT).offset(page * LIMIT)

    result = await session.execute(stmt)
    categories = result.scalars().all()

    return ListOneTypeCategories(
        categories=[cat.name for cat in categories]
    )


async def delete_category(session: AsyncSession, data: CategoryDto, user_uuid: uuid):
    await session.execute(
        delete(Category)
        .where(
            Category.user_uuid == user_uuid,
            Category.name == data.name,
            Category.type == data.type
        )
    )

import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.category import Category
from data.entities.user import User
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from models.categories.list_categories import ListCategories


async def add_expense(session: AsyncSession, data: CategoryDto, user_uuid: uuid):
    query = select(User).options(selectinload(User.categories)).filter_by(uuid=user_uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    new_category = Category(name=data.name, type=data.type, user_uuid=user_uuid)

    if len([cat.name for cat in user.categories if cat.type == data.type and cat.name == data.name]) > 0:
        raise DuplicatedEntryError("This category already exists")

    session.add(new_category)


async def get_categories(session: AsyncSession, user_uuid: str) -> ListCategories:
    query = select(User).options(selectinload(User.categories)).filter_by(uuid=user_uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    return ListCategories(
        categories_expenses=[cat.name for cat in user.categories if cat.type == "expenses"],
        categories_incomes=[cat.name for cat in user.categories if cat.type == "incomes"]
    )


async def update_category(session: AsyncSession, data: EditDto, user_uuid: uuid):
    if data.old_name == data.new_name:
        raise DuplicatedEntryError("This category already exists")
    await session.execute(
        update(Category)
        .where(
            Category.user_uuid == user_uuid,
            Category.name == data.old_name,
            Category.type == data.type
        )
        .values(name=data.new_name)
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

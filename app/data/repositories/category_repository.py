import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.category import Category
from data.entities.user import User
from exceptions.NoUserError import NoUserError
from models.categories.category import CategoryDto
from models.categories.list_categories import ListCategories


async def add_category(session: AsyncSession, data: CategoryDto, user_uuid: uuid):
    new_category = Category(name=data.name, type=data.type, user_uuid=user_uuid)
    session.add(new_category)


async def get_categories(session: AsyncSession, user_uuid: str) -> ListCategories:
    query = select(User).options(selectinload(User.categories)).filter_by(uuid=user_uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoUserError("The user does not exist")

    return ListCategories(
        categories_expenses=[cat.name for cat in user.categories if cat.type == "expenses"],
        categories_incomes=[cat.name for cat in user.categories if cat.type == "incomes"]
    )

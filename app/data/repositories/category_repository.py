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



async def update_category(session: AsyncSession, data: EditDto):
    await session.execute(
        update(Category)
        .where(
            Category.uuid == data.uuid,
        )
        .values(name=data.name)
    )


async def get_all_categories(session: AsyncSession,
                             user_uuid: str
                             ) -> ListCategories:
    expenses = {
        "name": [],
        "uuid": [],
        "count": 0
    }
    incomes = {
        "name": [],
        "uuid": [],
        "count": 0
    }
    categories = await session.execute(select(Category).order_by(Category.name).where(Category.user_uuid == user_uuid))
    for c in categories.scalars().all():
        if c.type == "expenses":
            if expenses["count"] < LIMIT:
                expenses["name"].append(c.name)
                expenses["uuid"].append(c.uuid)
            expenses["count"] += 1
        else:
            if incomes["count"] < LIMIT:
                incomes["name"].append(c.name)
                incomes["uuid"].append(c.uuid)
            incomes["count"] += 1


    return ListCategories(
        expenses=expenses["name"],
        e_uuids=expenses["uuid"],
        e_count=expenses["count"],
        incomes=incomes["name"],
        i_uuids=incomes["uuid"],
        i_count=incomes["count"]
    )


async def get_one_type_categories(session: AsyncSession,
                                  user_uuid: str,
                                  type: str,
                                  page,
                                  order
                                  ) -> ListOneTypeCategories:
    type = "expenses" if type == "e" else "incomes"
    stmt = select(Category)
    stmt = stmt.order_by(Category.name) if order else stmt.order_by(Category.name.desc())
    stmt = stmt.where(Category.user_uuid == user_uuid, Category.type == type).limit(LIMIT).offset(page * LIMIT)

    result = await session.execute(stmt)
    categories = result.scalars().all()

    return ListOneTypeCategories(
        categories=[cat.name for cat in categories],
        uuids=[cat.uuid for cat in categories]
    )


async def delete_category(session: AsyncSession, uuid, user_uuid: uuid):
    category = await session.execute(select(Category).where(Category.uuid == uuid))
    category = category.scalar_one_or_none()
    if not category:
        raise NoEntryError("This category does not exist")
    type = Expense if category.type == "expenses" else Income
    await session.execute(
        delete(type)
        .where(
            type.user_uuid == user_uuid,
            type.name == category.name,
        )
    )
    await session.execute(
        delete(Category)
        .where(Category.uuid == uuid)
    )


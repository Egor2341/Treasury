from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import expenses_repository
from models.statistics.item import ItemDto
from services.security import get_user_from_token

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"]
)


@router.get("", status_code=200)
async def get_expenses(
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    return await expenses_repository.get_expenses(session, current_user_uuid)


@router.post("", status_code=201)
async def add_expenses(
        data: ItemDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)

):
    await expenses_repository.add_expense(session, data, current_user_uuid)
    await session.commit()


@router.patch("", status_code=200)
async def edit_category(
        data: ItemDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await expenses_repository.edit_expense(session, data, current_user_uuid)
    await session.commit()


@router.delete("/{title}", status_code=200)
async def delete_categoty(
        title: str,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await expenses_repository.delete_expense(session, title, current_user_uuid)
    await session.commit()

# @router.get("/search", status_code=200)
# async def search(title: str, year: int, month: str):
#     pass

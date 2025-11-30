from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import incomes_repository
from models.statistics.item import ItemDto
from services.security import get_user_from_token

router = APIRouter(
    prefix="/api/incomes",
    tags=["incomes"]
)

@router.get("", status_code=200)
async def get_expenses(
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    return await incomes_repository.get_incomes(session, current_user_uuid)


@router.post("", status_code=201)
async def add_expenses(
        data: ItemDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)

):
    await incomes_repository.add_income(session, data, current_user_uuid)
    await session.commit()


@router.patch("", status_code=200)
async def edit_category(
        data: ItemDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await incomes_repository.edit_income(session, data, current_user_uuid)
    await session.commit()


@router.delete("/{title}", status_code=200)
async def delete_categoty(
        title: str,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await incomes_repository.delete_income(session, title, current_user_uuid)
    await session.commit()

# @router.get("/search", status_code=200)
# async def search(title: str, year: int, month: str):
#     pass
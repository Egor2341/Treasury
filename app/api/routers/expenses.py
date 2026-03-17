from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import expenses_repository
from models.statistics.item import ItemResponseDto
from services.security import get_user_from_token, RoleChecker

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"]
)


@router.get("", status_code=200)
async def get_expenses(
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session),
        page: int = 0,
        order: bool = True
):
    return await expenses_repository.get_expenses(
        session,
        current_user_uuid,
        page,
        order
    )

@router.get("/categories", status_code=200)
async def get_categories(
        user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    return await expenses_repository.get_categories(session, user_uuid)


@router.post("", status_code=201)
async def add_expenses(
        data: ItemResponseDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)

):
    await expenses_repository.add_expense(session, data, current_user_uuid)
    await session.commit()


@router.patch("", status_code=200)
async def edit_expense(
        data: ItemResponseDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await expenses_repository.edit_expense(session, data, current_user_uuid)
    await session.commit()


@router.delete("", status_code=200)
async def delete_expense(
        title: str,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await expenses_repository.delete_expense(session, title, current_user_uuid)
    await session.commit()


@router.get("/search", status_code=200)
async def search(title: str,
                 year: int,
                 month: str,
                 current_user_uuid: str = Depends(get_user_from_token),
                 session: AsyncSession = Depends(get_session)
                 ):
    return await expenses_repository.search_expense(title, year, month, current_user_uuid, session)

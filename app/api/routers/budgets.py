from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import budgets_repository
from models.budgets.budget import BudgetDto
from services.security import get_user_from_token

router = APIRouter(
    prefix="/api/budgets",
    tags=["budgets"]
)


@router.get("", status_code=200)
async def get_budgets(
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    return await budgets_repository.get_budgets(session, current_user_uuid)


@router.patch("", status_code=200)
async def edit_budget(
        data: BudgetDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await budgets_repository.edit_budgets(session, data, current_user_uuid)
    await session.commit()


@router.get("/search", status_code=200)
async def search(type: str, year: int, current_user_uuid: str = Depends(get_user_from_token),
                 session: AsyncSession = Depends(get_session)):
    return await budgets_repository.search_budgets(session, current_user_uuid, type, year)

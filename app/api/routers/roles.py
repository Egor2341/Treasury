from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import role_repository

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"]
)

@router.get("", status_code=200)
async def get_roles(
        session: AsyncSession = Depends(get_session)
):
    return await role_repository.get_roles(session)
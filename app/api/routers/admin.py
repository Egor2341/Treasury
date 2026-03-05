from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import user_repository
from models.admin.user import User
from services.security import RoleChecker

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

@router.post("/add", status_code=200)
async def add_admin(
        data: User,
        _: Annotated[str, Depends(RoleChecker(allowed_roles=["admin"]))],
        session: AsyncSession = Depends(get_session)
):
    await user_repository.add_admin(session, data.email)
    await session.commit()

@router.post("/delete", status_code=200)
async def delete_admin(
        data: User,
        _: Annotated[str, Depends(RoleChecker(allowed_roles=["admin"]))],
        session: AsyncSession = Depends(get_session)
):
    await user_repository.delete_admin(session, data.email)
    await session.commit()

@router.get("/users", status_code=200)
async def get_users(
        current_user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["admin"]))],
        session: AsyncSession = Depends(get_session)
):
    return await user_repository.get_users(session, current_user_uuid)

@router.get("/stat", status_code=200)
async def get_stat(type_data: str,
                 type_value: str,
                 year: int,
                 month: str,
                 _: Annotated[str, Depends(RoleChecker(allowed_roles=["admin"]))],
                 session: AsyncSession = Depends(get_session)
):
    return await user_repository.get_statistics(session, type_data, type_value, year, month)


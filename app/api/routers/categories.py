from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import category_repository
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from services.security import get_user_from_token, RoleChecker

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)


@router.get("", status_code=200)
async def get_categories(
        current_user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    return await category_repository.get_categories(session, current_user_uuid)

@router.post("", status_code=201)
async def new_category(
        data: CategoryDto,
        current_user: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    await category_repository.add_category(session, data, current_user)
    await session.commit()


@router.patch("", status_code=200)
async def edit_category(
        data: EditDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await category_repository.update_category(session, data, current_user_uuid)
    await session.commit()


@router.delete("", status_code=200)
async def delete_category(
        name: str,
        type: str,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await category_repository.delete_category(session, CategoryDto(name=name, type=type), current_user_uuid)
    await session.commit()

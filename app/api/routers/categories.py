from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import category_repository
from models.categories.category import CategoryDto
from models.categories.edit import EditDto
from services.alpha_vantage_service import ExchangeService
from services.security import RoleChecker

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

service = ExchangeService()

@router.get("/rates", status_code=200, response_model=None)
async def get_rates(_: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))]):
    return await service.get_rates()

@router.get("", status_code=200)
async def get_all_categories(
        current_user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session),
):
    return await category_repository.get_all_categories(
        session,
        current_user_uuid,
    )


@router.get("/one_type", status_code=200)
async def get_one_type_categories(
        type: str,
        current_user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session),
        page: int = 0,
        order: bool = True
):
    return await category_repository.get_one_type_categories(
        session,
        current_user_uuid,
        type,
        page,
        order
    )


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
        _: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    await category_repository.update_category(session, data)
    await session.commit()


@router.delete("", status_code=200)
async def delete_category(
        uuid: str,
        current_user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    await category_repository.delete_category(session, uuid, current_user_uuid)
    await session.commit()

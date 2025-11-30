from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import category_repository
from models.categories.category import CategoryDto
from models.categories.edit import Edit
from services.security import get_user_from_token

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("", status_code=200)
async def get_categories(
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    return await category_repository.get_categories(session, current_user_uuid)

@router.post("", status_code=201)
async def new_category(
        data: CategoryDto,
        current_user_uuid: str = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_session)
):
    await category_repository.add_category(session, data, current_user_uuid)
    await session.commit()

@router.patch("", status_code=200)
async def edit_category(data: Edit):
    pass

@router.delete("/{title}/", status_code=200)
async def delete_category(title: str, type: str):
    pass

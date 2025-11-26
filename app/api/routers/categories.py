from fastapi import APIRouter

from entities.categories.category import Category
from entities.categories.edit import Edit

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("", status_code=200)
async def get_categories():
    pass

@router.post("", status_code=201)
async def new_category(data: Category):
    pass

@router.patch("", status_code=200)
async def edit_category(data: Edit):
    pass

@router.delete("/{title}/", status_code=200)
async def delete_category(title: str, type: str):
    pass

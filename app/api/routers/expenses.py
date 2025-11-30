from fastapi import APIRouter
from fastapi.params import Depends

from models.statistics.category import Category
from services.security import get_user_from_token

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"]
)

@router.get("", status_code=200)
async def get_expenses():
    pass

@router.post("", status_code=201)
async def add_expenses(current_user: str = Depends(get_user_from_token)):
    pass

@router.patch("", status_code=200)
async def edit_category(data: Category):
    pass

@router.delete("/{title}", status_code=200)
async def delete_categoty(title: str):
    pass

@router.get("/search", status_code=200)
async def search(title: str, year: int, month: str):
    pass
from fastapi import APIRouter

from models.statistics.category import Category

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"]
)

@router.get("", status_code=200)
async def get_expenses():
    pass

@router.post("", status_code=201)
async def add_expences():
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
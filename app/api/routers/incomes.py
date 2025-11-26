from fastapi import APIRouter

from entities.statistics.category import Category

router = APIRouter(
    prefix="/api/incomes",
    tags=["incomes"]
)

@router.get("", status_code=200)
async def get_incomes():
    pass

@router.post("", status_code=201)
async def add_incomes():
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
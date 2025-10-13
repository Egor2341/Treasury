from fastapi import APIRouter

from app.entities.budgets.edit import Edit

router = APIRouter(
    prefix="/api/budgets",
    tags=["budgets"]
)

@router.get("", status_code=200)
async def get_budgets():
    pass

@router.patch("", status_code=200)
async def edit_budget(new_sum: Edit):
    pass

@router.get("/{name}/search", status_code=200)
async def search(name: str, year: int):
    pass


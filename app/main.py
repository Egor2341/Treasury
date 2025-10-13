from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.budgets import router as budgets_router
from app.api.routers.categories import router as categories_router
from app.api.routers.expenses import router as expenses_router
from app.api.routers.incomes import router as incomes_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(incomes_router)
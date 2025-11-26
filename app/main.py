import asyncio

import typer
from fastapi import FastAPI

from api.routers.auth import router as auth_router
from api.routers.budgets import router as budgets_router
from api.routers.categories import router as categories_router
from api.routers.expenses import router as expenses_router
from api.routers.incomes import router as incomes_router
from data.init_bd import init_models

app = FastAPI()

app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(incomes_router)

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == "__main__":
    cli()

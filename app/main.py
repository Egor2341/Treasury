import typer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.auth import router as auth_router
from api.routers.budgets import router as budgets_router
from api.routers.categories import router as categories_router
from api.routers.expenses import router as expenses_router
from api.routers.incomes import router as incomes_router
from api.routers.roles import router as roles_router
from api.routers.admin import router as admin_router
from dotenv import load_dotenv

load_dotenv()



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(incomes_router)
app.include_router(roles_router)
app.include_router(admin_router)

cli = typer.Typer()


@cli.command()
def db_init_models():
    print("Done")


if __name__ == "__main__":
    cli()

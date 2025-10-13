from fastapi import APIRouter, Response

from app.entities.auth.login import Login
from app.entities.auth.register import Register

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register(data: Register):
    pass

@router.post("/login", status_code=200)
async def login(response: Response, data: Login):
    pass
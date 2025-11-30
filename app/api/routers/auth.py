from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import user_repository
from models.auth.login import Login
from models.auth.login_response import LoginResponse
from models.auth.register import Register
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoUserError import NoUserError
from services.security import create_jwt_token

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post("/register", status_code=201)
async def register(data: Register, session: AsyncSession = Depends(get_session)):
    await user_repository.add_user(session, data)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise DuplicatedEntryError("The user is already stored")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await user_repository.get_user(session, form_data.username, form_data.password)
    if not user:
        raise NoUserError("User not exist")

    token = create_jwt_token({"sub": user.uuid})
    return LoginResponse(token=token, token_type="bearer")
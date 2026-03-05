from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import user_repository
from models.auth.login import Login
from models.auth.login_response import AuthResponse
from models.auth.refresh_token import RefreshTokenRequest
from models.auth.register import Register
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoEntryError import NoEntryError
from services.security import create_access_token, create_refresh_token, get_user_from_token

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


@router.post("/login", status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await user_repository.get_user(session, form_data.username, form_data.password)
    if not user:
        raise NoEntryError("User not exist")


    access_token = create_access_token({"sub": user.uuid, "roles": [r.name for r in user.roles]})
    refresh_token = create_refresh_token({"sub": user.uuid})
    return AuthResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", status_code=200)
async def refresh_token(request: RefreshTokenRequest, session: AsyncSession = Depends(get_session)):
    user = await user_repository.get_user_by_uuid(session, get_user_from_token(request.refresh_token))
    if not user:
        raise NoEntryError("User not exist")

    access_token = create_access_token({"sub": user.uuid, "roles": [r.name for r in user.roles]})
    return AuthResponse(access_token=access_token, refresh_token=request.refresh_token, token_type="bearer")

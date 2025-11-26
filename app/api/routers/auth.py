from fastapi import APIRouter, Response, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from data.init_bd import get_session
from data.repositories import user_repository
from entities.auth.login import Login
from entities.auth.register import Register
from exceptions.DuplicateEntryError import DuplicatedEntryError
from exceptions.NoUserError import NoUserError

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register(data: Register, session: AsyncSession = Depends(get_session)):
    user = user_repository.add_user(session, data)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The user is already stored")

@router.post("/login", status_code=200)
async def login(response: Response, data: Login, session: AsyncSession = Depends(get_session)):
    user = user_repository.get_user(session, data)
    if user is None:
        raise NoUserError("The user is not exist")
    else:
        return user

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data.entities.role import Role
from data.entities.user import User
from exceptions.NoEntryError import NoEntryError
from models.admin.user_info import UserInfo
from models.auth.register import Register

from passlib.context import CryptContext
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, plain_password)


async def add_user(session: AsyncSession, data: Register):
    new_user = User(email=data.email, password=hash_password(data.password.get_secret_value()))
    query = select(Role).filter_by(name="user")
    result = await session.execute(query)
    role = result.scalar_one_or_none()
    if role is None:
        raise NoEntryError("The role does not exist")
    new_user.roles.append(role)
    session.add(new_user)


async def get_user(session: AsyncSession, email: str, password: str) -> User | None:
    query = select(User).options(selectinload(User.roles)).filter_by(email=email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user


async def get_user_by_uuid(session: AsyncSession, uuid: str) -> User | None:
    query = select(User).filter_by(uuid=uuid)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        return None

    return user


async def get_users(session: AsyncSession, limit: int = 10, offset: int = 0) -> List[UserInfo]:
    stmt = (
        select(User)
        .options(selectinload(User.roles))
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(stmt)
    users = result.scalars().all()

    mapped_users = []
    for user in users:
        if user.email != "admin@treasury.com":
            mapped_users.append(UserInfo(email=user.email, roles=[r.name for r in user.roles]))

    return mapped_users



async def add_admin(session: AsyncSession, email: str) -> None:
    query = select(User).options(selectinload(User.roles)).filter_by(email=email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    query = select(Role).filter_by(name="admin")
    result = await session.execute(query)
    role = result.scalar_one_or_none()
    if role is None:
        raise NoEntryError("The role does not exist")

    user.roles.append(role)


async def delete_admin(session: AsyncSession, email: str) -> None:
    # admin cannot delete the first admin
    if email == "admin@treasury.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions")

    query = select(User).options(selectinload(User.roles)).filter_by(email=email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise NoEntryError("The user does not exist")

    roles = user.roles
    for i in range(len(roles)):
        if roles[i].name == "admin":
            roles.pop(i)
            break

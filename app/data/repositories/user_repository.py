from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.entities.user import User
from models.auth.login import Login
from models.auth.register import Register

from passlib.context import CryptContext
from werkzeug.security import generate_password_hash, check_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, plain_password)


async def add_user(session: AsyncSession, data: Register):
    new_user = User(email=data.email, password=hash_password(data.password.get_secret_value()))
    session.add(new_user)


async def get_user(session: AsyncSession, email: str, password: str) -> User | None:
    query = select(User).filter_by(email=email)
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



from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.entities.user import User
from models.auth.login import Login
from models.auth.register import Register

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def add_user(session: AsyncSession, data: Register):
    new_user = User(email=data.email, name=data.name, password=hash_password(data.password.get_secret_value()))
    session.add(new_user)
    return new_user


async def get_user(session: AsyncSession, data: Login) -> bool:
    query = select(User).filter_by(email=data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        return False

    if not verify_password(data.password.get_secret_value(), user.password):
        return False

    return True

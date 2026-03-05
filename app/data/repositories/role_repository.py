from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.entities.role import Role
from models.auth.roles import Roles


async def get_roles(session: AsyncSession) -> Roles:
    result = await session.execute(select(Role))

    return Roles(roles=[r[0].name for r in result.all()])
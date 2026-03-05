import uuid
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base


class Role(Base):
    __tablename__ = "roles"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

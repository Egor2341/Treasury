import uuid
from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base


class Category(Base):
    __tablename__ = "categories"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(16))
    user_uuid: Mapped[uuid] = mapped_column(ForeignKey("users.uuid"))

    user: Mapped["User"] = relationship(back_populates="categories")



from data.entities.user import User

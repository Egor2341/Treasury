import uuid

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey, DECIMAL, Integer, String
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base
from decimal import Decimal


class Expense(Base):
    __tablename__ = "expenses"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_uuid: Mapped[uuid] = mapped_column(ForeignKey("users.uuid"))
    name: Mapped[str] = mapped_column(String(64))
    value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    month: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship(back_populates="expenses")


from data.entities.user import User

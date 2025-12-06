import uuid

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey, DECIMAL, Integer, String
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base
from decimal import Decimal


class Budget(Base):
    __tablename__ = "budgets"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_uuid: Mapped[uuid] = mapped_column(ForeignKey("users.uuid"))
    type: Mapped[str] = mapped_column(String(16))
    month: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    user: Mapped["User"] = relationship(back_populates="budgets")


from data.entities.user import User

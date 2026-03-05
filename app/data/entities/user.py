import uuid
from typing import List

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base

association_table = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.uuid")),
    Column("role_id", ForeignKey("roles.uuid")),
)

class User(Base):
    __tablename__ = "users"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(164))

    roles: Mapped[List["Role"]] = relationship(secondary=association_table)


    categories: Mapped[List["Category"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan, delete"
    )

    expenses: Mapped[List["Expense"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    incomes: Mapped[List["Income"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    budgets: Mapped[List["Budget"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


from data.entities.category import Category
from data.entities.expense import Expense
from data.entities.incomes import Income
from data.entities.budget import Budget
from data.entities.role import Role

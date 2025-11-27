from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from data.init_bd import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)

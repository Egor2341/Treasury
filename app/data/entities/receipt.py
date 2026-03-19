import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.testing.schema import mapped_column

from data.init_bd import Base


class Receipt(Base):
    __tablename__ = "receipts"

    uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    object_name: Mapped[str] = mapped_column(String(128))
    original_name: Mapped[str] = mapped_column(String(128))
    content_type: Mapped[str] = mapped_column(String(128))
    user_uuid: Mapped[uuid] = mapped_column(ForeignKey("users.uuid"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped["User"] = relationship(back_populates="receipts")



from data.entities.user import User

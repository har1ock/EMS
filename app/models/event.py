from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Event(Base):
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)

    # Зовнішній ключ: вказує на id в таблиці "users"
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Зв'язок (Relationship): дозволить в коді писати event.owner і отримувати об'єкт юзера
    owner: Mapped["User"] = relationship("User", back_populates="events")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from app.database import  Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.event import Event


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user")
    
    events: Mapped[list["Event"]] = relationship("Event", back_populates="owner", cascade="all, delete-orphan")
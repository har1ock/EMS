from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title =Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    location = Column(String, nullable=False)

    # Зовнішній ключ: вказує на id в таблиці "users"
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Зв'язок (Relationship): дозволить в коді писати event.owner і отримувати об'єкт юзера
    owner = relationship("User", back_populates="events")

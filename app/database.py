
from app.core.config import settings
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session


# Створення двигуна SQLAlchemy для взаємодії з SQLite.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Налаштування фабрики сесій для генерації підключень до бази даних.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """Декларативна база, від якої будуть успадковуватися всі моделі таблиць проєкту."""
    pass

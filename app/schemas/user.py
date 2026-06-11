from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    """Схема валідації вхідних даних для створення (реєстрації) нового користувача."""
    email: EmailStr # Автоматично перевіряє коректність формату електронної пошти
    password: str


class UserOut(BaseModel):
    """Схема структури відповіді сервера, яка приховує приватні дані (наприклад, хеш пароля)."""
    # Автоматичне перетворення об'єктів моделі бази даних SQLAlchemy у формат JSON
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str

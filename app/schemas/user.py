from pydantic import BaseModel, EmailStr
from typing import Optional


# Те, що ми очікуємо від клієнта при реєстрації
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Те, що ми повертаємо клієнту
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        # Дозволяє Pydantic читати дані з SQLAlchemy моделей
        from_attributes = True 

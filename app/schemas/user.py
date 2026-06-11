from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# Те, що ми очікуємо від клієнта при реєстрації
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Те, що ми повертаємо клієнту
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str

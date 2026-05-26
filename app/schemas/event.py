from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Те що надає клієнт 
class  EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: str

# Повертаємо клієнту
class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: datetime
    location: str
    owner_id: int

    class Config:
        from_attributes = True
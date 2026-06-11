from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime, timezone
from typing import Optional



class EventCreate(BaseModel):
    """Схема валідації вхідних даних при створенні нової події."""
    title: str
    description: Optional[str] = None
    date: datetime
    location: str

    @field_validator("date")
    @classmethod
    def check_date_is_future(cls, value: datetime) -> datetime:
        """Перевірка, дата повинна бути в майбутньому"""
        current_time = datetime.now(timezone.utc)
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value < current_time:
            raise ValueError("Подія повинна бути в майбутньому")
        return value


class EventUpdate(BaseModel):
    """Схема валідації даних для часткового або повного оновлення існуючої події."""
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

    @field_validator("date")
    @classmethod
    def check_date_is_future(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is not None:
            current_time = datetime.now(value.tzinfo or timezone.utc)
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            if value < current_time:
                raise ValueError("Подія повинна бути в майбутньому")
        return value


class EventOut(BaseModel):
    """Схема структури вихідних JSON-даних (відповіді сервера) для об'єкта події."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    date: datetime
    location: str
    owner_id: int
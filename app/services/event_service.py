from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


def create_new_event(db: Session, event_data: EventCreate, owner_id: int) -> Event:
    """
    Створити нову подію в базі даних та прив'язує її до користувача 
    """
    db_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        location=event_data.location,
        owner_id=owner_id # Записуємо ID поточного авторизованого користувача
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_id(db: Session, event_id: int) -> Event | None:
    """
    Шукає подію в базі даних за її ID. 
    Повертає об'єкт події або None, якщо нічого не знайдено.
    """
    return db.query(Event).filter(Event.id == event_id).first()

def get_event_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    location: Optional[str] = None
) -> List[Event]:
    """
    Повертає список подій з підтримкою пагінації та фільтрації за локацією
    """
    query = db.query(Event)
    
    if location:
        query = query.filter(Event.location.ilike(f"%{location}"))
    
    return query.offset(skip).limit(limit).all()

def update_event(db: Session, db_event: Event, update_data: EventUpdate) -> Event:
    """
    Оновлює поля події новими даними, які прийшли від клієнта.
    """    
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, db_event: Event) -> None:
    """
    Видаляє подію з бази даних.
    """
    db.delete(db_event)
    db.commit()
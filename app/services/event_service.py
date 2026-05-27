from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate

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
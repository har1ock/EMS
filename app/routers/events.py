from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.schemas.event import EventCreate, EventOut
from app.models.user import User
from app.services import event_service


router = APIRouter(
    prefix="/event",
    tags=["Events"]
)

@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Створення нової події доступне тільки авторизованим користувачам.
    """
    return event_service.create_new_event(db, event_data=event_data, owner_id=current_user.id)


@router.get("/{id}", response_model=EventOut)
def read_event(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отримання детальної інформації про подію за її ID.
    Доступно будь-якому авторизованому користувачу.
    """
    db_event = event_service.get_event_by_id(db, event_id=id)

    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подію за ID {id} не знайдено"
        )
    
    return db_event
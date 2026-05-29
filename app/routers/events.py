from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user, require_admin
from app.schemas.event import EventCreate, EventOut, EventUpdate
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

@router.put("/{id}", response_model=EventOut)
def update_existing_event(id: int, 
                          event_data: EventUpdate, 
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)
    ):
    """
    Редагування події. Доступно тільки власнику цієї події
    """
    db_event = event_service.get_event_by_id(db, event_id=id)

    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подію з ID {id} не знайдено."
        )
    
    if db_event.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ви не є власником цієї події. Редагування заборонено."
        )

    return event_service.update_event(db, db_event=db_event, update_data=event_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_event(
    id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin) # Перевірка: сюди пройде тільки адмін!
):
    """
    Видалення події за її ID. Доступно ТІЛЬКИ користувачам з роллю 'admin'.
    Повертає статус 204 No Content у разі успіху.
    """
    # 1. Шукаємо подію в базі
    db_event = event_service.get_event_by_id(db, event_id=id)
    
    # 2. Якщо її немає — 404 Not Found
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Подію з ID {id} не знайдено."
        )
        
    # 3. Викликаємо сервіс для видалення
    event_service.delete_event(db, db_event=db_event)
    
    # Коли ми повертаємо статус 204 (No Content), тіло відповіді має бути порожнім.
    # FastAPI автоматично це згенерує, тому просто пишемо return
    return None
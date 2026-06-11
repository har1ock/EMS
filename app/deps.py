from typing import Generator
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.services import user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_db() -> Generator[Session, None, None]:
    """Створює окрему сесію БД для кожного HTTP-запиту та гарантовано закриває її після завершення."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)      
) -> User:
    """Витягує JWT-токен із заголовка Authorization, валідує його та повертає поточного користувача."""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані (токен недійсний або просрочений)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Розшифровуємо токен за допомогою секретного ключа
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    # Шукаємо користувача в базі. Якщо його видалили, але токен ще діє — доступ буде відхилено
    user = user_service.get_user_by_email(db, email=email)
    if user is None:
        raise credential_exception
    
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Залежність для перевірки, чи має користувач права адміністратора.
    Якщо роль не 'admin' — повертає помилку 403 Forbidden.
    """
    if str(current_user.role) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас немає прав для виконання цієї дії. Потрібна роль 'admin'.",
        )
    return current_user
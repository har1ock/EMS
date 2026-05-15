from typing import Generator
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.services import user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)      
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані (токен недійсний або просрочений)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    user = user_service.get_user_by_email(db, email=email)
    if user is None:
        raise credential_exception
    
    return user
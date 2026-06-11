from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.services import user_service
from app.deps import get_db, get_current_user, require_admin
from app.core.security import create_access_token, verify_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    # Викликаємо сервіс для перевірки
    db_user = user_service.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Викликаємо сервіс для створення
    return user_service.create_new_user(db, user_data=user_data)

# Аутентифікація користувача та видача доступу
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_email(db, email=form_data.username)

    # Верифікація пароля за допомогою інструменту безпеки (хешу Argon2)
    if not user or not verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    # Генерація сесійного JWT-токена
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin-only-dashboard")
def get_admin_dashboard(admin_user: User = Depends(require_admin)):
    """
    Цей ендпоінт доступний тільки користувачам з роллю 'admin'.
    """
    return {
        "message": f"Вітаємо у секретній адмінці, {admin_user.email}!",
        "secret_data": "Тут якась важлива статистика бекенду"
    }


@router.patch("/make-me-admin")
@router.patch("/make-admin/{user_id}", response_model=UserOut)
def promote_user_to_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Адмінський ендпоінт для призначення іншого користувача адміністратором.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    setattr(db_user, "role", "admin")
    db.commit()
    db.refresh(db_user)
    return db_user
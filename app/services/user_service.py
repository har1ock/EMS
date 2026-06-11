from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """Пошук користувача в базі даних за його email."""
    return db.query(User).filter(User.email == email).first()

def create_new_user(db: Session, user_data: UserCreate):
    # Хешуємо пароль перед збереженням в базу
    hashed_pwd = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_pwd,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def make_user_admin(db: Session, db_user: User) -> User:
    """
    Змінює роль користувача на 'admin' в базі даних.
    """
    setattr(db_user, "role", "admin") 
    db.commit()
    db.refresh(db_user)
    return db_user
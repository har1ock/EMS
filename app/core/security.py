from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

# Налаштування алгоритму хешування
ph = PasswordHasher()

def get_password_hash(password: str) -> str:
    """Генерація безпечного хешу для переданого пароля."""
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевірка відповідності введеного пароля його збереженому хешу."""
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    
def create_access_token(data: dict):
    """Створення сесійного JWT-токена для авторизації користувача."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt
import os

class Settings:
    PROJECT_NAME: str = "Event Managment System"
    DATABASE_URL: str = "sqlite:///.app.db"
    SECRET_KEY: str = "SUPER_SECRET_KEY_123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
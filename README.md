# Event Management API

RESTful API для керування подіями з вбудованою системою автентифікації користувачів, рольовою моделлю доступу (RBAC), NoSQL-кешуванням та повною контейнеризацією розгортання.

## Стек технологій

* **Фреймворк:** FastAPI (Python 3.11)
* **ОРМ & База даних:** SQLAlchemy + Alembic (Міграції) + SQLite
* **Безпека:** JWT (JSON Web Tokens) + Хешування паролів Argon2
* **Оптимізація:** Redis (FastAPI-Cache2) для NoSQL-кешування списків
* **Моніторинг:** Кастомний Middleware для логування часу виконання запитів
* **Тестування:** Pytest (In-Memory БД для ізоляції тестів)
* **Оркестрація:** Docker + Docker Compose

## Структура проекту

```text
├── app/
│   ├── core/          # Конфігурація (config.py) та безпека (security.py)
│   ├── models/        # SQLAlchemy моделі таблиць БД (user.py, event.py)
│   ├── schemas/       # Pydantic схеми валідації даних (user.py, event.py)
│   ├── services/      # Шар бізнес-логіки (user_service.py, event_service.py)
│   ├── routers/       # Ендпоінти API (users.py, events.py)
│   ├── database.py    # Налаштування підключення та сесій двигуна ORM
│   ├── deps.py        # Залежності (введення сесії БД, авторизація, адмін-права)
│   └── main.py        # Головний файл додатка, ініціалізація Redis, Middleware логера
├── tests/             # Автоматичні тести (conftest.py, test_*.py)
├── Dockerfile         # Рецепт збірки образу для Python додатка
├── docker-compose.yml # Оркестрація контейнерів додатка та Redis в одну мережу
├── .dockerignore      # Фільтр сміття для Docker
├── EMS.postman_collection.json # Експортована колекція запитів для Postman
├── pyproject.toml              # Конфігурація середовища тестування (налаштування pythonpath для pytest)
└── requirements.txt   # Залежності проєкту
```

## Запуск

* Найшвидший спосіб підняти додаток разом із Redis в ізольованій мережі. Переконайтеся, що у вас запущено Docker Desktop, і виконайте в корені проєкту:
```bash
docker compose up --build
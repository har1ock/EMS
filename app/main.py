import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.routers import users, events

# Налаштування базового логера Python для виведення повідомлень у консоль Docker
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("API-Logger")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Event Managment API", lifespan=lifespan)

# Middleware для перехоплення та логування запитів
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | Time: {process_time:.2f}ms"
    )
    
    return response

app.include_router(users.router)
app.include_router(events.router)

@app.get("/")
def root():
    """Базовий кореневий ендпоінт для перевірки працездатності сервісу (Health Check)."""
    return {"message": "Api is running"}

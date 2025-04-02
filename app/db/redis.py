import redis.asyncio as redis

from app.config.settings import settings


redis_db = redis.Redis(
    host=settings.REDIS_HOST,
    password=settings.REDIS_PASSWORD,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

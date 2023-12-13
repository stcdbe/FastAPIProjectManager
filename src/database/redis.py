from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config import REDIS_URL


async def init_redis() -> None:
    redis = aioredis.from_url(REDIS_URL,
                              encoding='utf8',
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')

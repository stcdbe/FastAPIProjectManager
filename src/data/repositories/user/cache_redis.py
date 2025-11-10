import asyncio
import zlib
from datetime import timedelta
from uuid import UUID

import orjson
from redis.asyncio import Redis as AsyncRedis

from src.data.repositories.user.cashe_base import AbstractUserCacheRepository
from src.data.repositories.user.converters import convert_user_map_to_entity
from src.domain.user.entities import User


class RedisUserCasheRepository(AbstractUserCacheRepository):
    __slots__ = ("_key", "_redis")

    def __init__(self, redis: AsyncRedis) -> None:
        self._redis = redis
        self._key = "cache:user:{guid}"

    async def add_one(self, user: User) -> None:
        await self._redis.set(
            self._key.format(guid=user.guid),
            await asyncio.to_thread(zlib.compress, orjson.dumps(user)),
            ex=timedelta(seconds=60),
        )

    async def get_one(self, guid: UUID) -> User | None:
        res: bytes | None = await self._redis.get(self._key.format(guid=guid))  # type: ignore

        if res is None:
            return None

        decompressed_user_dict_str = await asyncio.to_thread(zlib.decompress, res)
        user_dict = orjson.loads(decompressed_user_dict_str)
        return convert_user_map_to_entity(user_dict)

    async def delete_one(self, guid: UUID) -> None:
        await self._redis.delete(self._key.format(guid=guid))

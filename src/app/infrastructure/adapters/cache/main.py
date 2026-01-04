from typing import Any

import redis.asyncio as aioredis


class Cache:
    def __init__(self, redis: aioredis.Redis) -> None:
        self._redis = redis

    async def set(self, key: str, value: Any, ex: int = 86400) -> None:
        await self._redis.set(key, value, ex=ex)

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

import orjson
from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from app.core.constants import DEFAULT_REDIS_TIMEOUT
from settings.config import AppSettings


async def initialize_redis_connection(redis: Redis) -> None:  # type: ignore[type-arg]
    try:
        await redis.initialize()
    except Exception as error:
        logger.critical("failed to initialize redis connection", error=repr(error))


async def close_redis_connection(redis: Redis) -> None:  # type: ignore[type-arg]
    logger.info("closing connection to redis...")
    try:
        await redis.close()
    except Exception as error:
        logger.warning("failed to close redis connection", error=repr(error))
    else:
        logger.info("connection to redis closed")


def create_redis_connection(settings: AppSettings) -> Redis:  # type: ignore[type-arg]
    connection_pool = ConnectionPool.from_url(str(settings.redis_url))  # type: ignore[var-annotated]
    return Redis(connection_pool=connection_pool, socket_timeout=DEFAULT_REDIS_TIMEOUT)


@dataclass
class CacheDatabase:
    _failed_to_serialize_msg = "failed to serialize value from redis"
    redis_client: Redis  # type: ignore[type-arg]

    async def set_data(self, key: str, data: Any, expire: timedelta) -> None:
        await self.redis_client.set(
            key,
            self._serialize(data),
            expire,
        )

    async def get_data(
        self,
        key: str,
    ) -> Any:
        data = await self.redis_client.get(key)
        if data is None:
            return None

        try:
            data = orjson.loads(data)
            if isinstance(data, dict):
                data = {int(key) if key.isdigit() else key: value for key, value in data.items()}
        except ValueError as error:
            logger.warning(self._failed_to_serialize_msg, error=repr(error), key=key)
            return None

        return data

    @staticmethod
    def _serialize(data: Any) -> bytes:
        return orjson.dumps(data, option=orjson.OPT_NON_STR_KEYS)

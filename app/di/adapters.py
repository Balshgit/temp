from typing import AsyncGenerator

from dependency_injector import containers, providers
from dependency_injector.providers import Resource, Singleton
from redis.asyncio import Redis

from app.infra.adapters.redis_cache import (
    CacheDatabase,
    close_redis_connection,
    create_redis_connection,
    initialize_redis_connection,
)
from app.infra.database.db_adapter import Database
from settings.config import AppSettings


async def initialize_database(database: Database) -> AsyncGenerator[Database, None]:
    yield database
    await database.disconnect()


async def initialize_redis_client(redis_client: Redis) -> AsyncGenerator[Redis, None]:  # type: ignore[type-arg]
    await initialize_redis_connection(redis_client)
    yield redis_client
    await close_redis_connection(redis_client)


class AdaptersContainer(containers.DeclarativeContainer):
    settings: providers.Dependency[AppSettings] = providers.Dependency()

    _database: Singleton[Database] = Singleton(
        Database,
        settings=settings,
    )
    database: Resource[Database] = Resource(initialize_database, database=_database)

    _redis_client: Singleton[Redis] = Singleton(  # type: ignore[type-arg]
        create_redis_connection,
        settings=settings,
    )
    redis_client = Resource(
        initialize_redis_client,
        redis_client=_redis_client,
    )
    cache_adapter: Singleton[CacheDatabase] = Singleton(CacheDatabase, redis_client=redis_client)

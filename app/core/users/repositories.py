from dataclasses import asdict, dataclass
from datetime import timedelta

from loguru import logger
from sqlalchemy import select, update

from app.core.users.dto import UpdateUserRequestDTO, UserDTO
from app.core.users.models import User
from app.infra.adapters.redis_cache import CacheDatabase
from app.infra.database.db_adapter import Database


@dataclass
class UserRepository:
    db: Database

    async def get_all_users(self) -> list[User]:
        query = select(User).order_by(User.id)

        async with self.db.session() as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        async with self.db.session() as session:
            result = await session.execute(query)
            return result.scalar_one()

    async def update_user_info(self, user_data: UpdateUserRequestDTO, user_id: int) -> None:
        values = {field: value for field, value in asdict(user_data).items() if field is not None}
        query = update(User).values(**values).where(User.id == user_id)

        async with self.db.session() as session:
            await session.execute(query)
            await session.commit()


@dataclass
class UserCacheRepository:
    cache_adapter: CacheDatabase

    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        key = self._build_user_key(user_id=user_id)
        data = await self.cache_adapter.get_data(key=key)

        if data is None:
            return None

        try:
            return UserDTO(**data)
        except ValueError as error:
            logger.warning("failed to get detailed user from cache", exc_info=error, user_id=user_id)
            return None

    async def set_user_to_cache(self, data: UserDTO) -> None:
        key = self._build_user_key(user_id=data.id)

        await self.cache_adapter.set_data(data=asdict(data), key=key, expire=timedelta(minutes=10))

    @staticmethod
    def _build_user_key(user_id: int) -> str:
        return f"users:{user_id}"

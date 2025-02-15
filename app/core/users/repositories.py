from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.core.users.models import User
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


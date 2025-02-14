from dataclasses import dataclass

from sqlalchemy import select

from app.core.users.models import User
from app.infra.database.db_adapter import Database


@dataclass
class UserRepository:
    db: Database

    async def get_all_users(self) -> list[User]:
        query = select(User)

        async with self.db.session as session:
            result = await session.execute(query)
            return result.scalars().all()
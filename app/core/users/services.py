from dataclasses import dataclass

from app.core.users.models import User
from app.core.users.repositories import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.user_repository.get_user_by_id(user_id=user_id)

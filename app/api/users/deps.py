from fastapi import Depends
from starlette.requests import Request

from app.core.users.repositories import UserRepository
from app.core.users.services import UserService


async def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(db=request.app.state.database)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository=user_repository)

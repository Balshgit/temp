from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.requests import Request

from app.core.users.repositories import UserRepository
from app.core.users.services import UserService
from settings.config import AppSettings


USER_KEY_HEADER = "USER-API-KEY"
api_key = APIKeyHeader(name=USER_KEY_HEADER, scheme_name=USER_KEY_HEADER, auto_error=True)


def request_verification(request: Request, api_key: str = Depends(api_key)) -> None:
    settings: AppSettings = request.app.state.settings
    if api_key != settings.USER_KEY_HEADER.get_secret_value():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


async def get_user_repository(request: Request) -> UserRepository:
    return UserRepository(db=request.app.state.database)


async def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository=user_repository)

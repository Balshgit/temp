from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.responses import JSONResponse

from app.api.users.deps import get_user_service, request_verification
from app.api.users.serializers import UserSerializer, DetailedUserSerializer
from app.core.users.services import UserService

router = APIRouter()


@router.get(
    "/users",
    name="users:get_users",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse,
    response_model=list[UserSerializer],
    dependencies=[Depends(request_verification)],
    summary="Получение всех пользователей",
)
async def get_users(user_service: UserService = Depends(get_user_service)) -> JSONResponse:
    """Получить список всех пользователей"""
    users = await user_service.get_all_users()

    data = [UserSerializer.model_validate(user).model_dump() for user in users]

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@router.get(
    "/users/{user_id}",
    name="users:get_users",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse,
    response_model=DetailedUserSerializer,
    dependencies=[Depends(request_verification)],
    summary="Получение всех пользователей",
)
async def get_users(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
) -> JSONResponse:
    """Получить список всех пользователей"""

    try:
        user = await user_service.get_user_by_id(user_id=user_id)
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail=f"User with user_id {user_id} not found") from exc

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=DetailedUserSerializer.model_validate(user).model_dump(),
    )

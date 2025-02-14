from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.api.users.deps import get_user_service
from app.api.users.serializers import UserSerializer
from app.core.users.services import UserService

router = APIRouter()


router.get(
    "/users",
    name="users:get_users",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse,
    response_model=list[UserSerializer],
    summary="Получение всех пользователей",
)
async def get_users(
    user_service: UserService = Depends(get_user_service)
) -> JSONResponse:
    """Получить список всех пользователей"""
    users = await user_service.get_all_users()

    data = [UserSerializer.model_dump(user) for user in users]

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

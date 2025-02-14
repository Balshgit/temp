from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.api.users.controllers import router as users_router


api_router = APIRouter(
    prefix="/api",
    default_response_class=ORJSONResponse,
)

api_router.include_router(users_router, tags=["users"])

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSerializer(BaseModel):
    id: int = Field(..., gt=0, title="Id пользователя")
    username: str = Field(..., title="Никнейм пользователя")
    first_name: str = Field(..., title="Имя пользователя")
    last_name: str = Field(..., title="Фамилия пользователя")

    model_config = ConfigDict(from_attributes=True)


class DetailedUserSerializer(BaseModel):
    id: int = Field(..., gt=0, title="Id пользователя")
    username: str = Field(..., title="Никнейм пользователя")
    first_name: str | None = Field(..., title="Имя пользователя")
    last_name: str | None = Field(..., title="Фамилия пользователя")
    email: EmailStr = Field(..., title="Почта пользователя")
    is_active: bool = Field(..., title="Активен ли пользователь")

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSerializer(BaseModel):
    username: str | None = Field(default=None, title="Никнейм пользователя")
    first_name: str | None = Field(default=None, title="Имя пользователя")
    last_name: str | None = Field(default=None, title="Фамилия пользователя")
    email: EmailStr | None = Field(default=None, title="Почта пользователя")

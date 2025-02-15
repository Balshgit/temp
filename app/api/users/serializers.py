from pydantic import BaseModel, ConfigDict, Field


class UserSerializer(BaseModel):
    id: int = Field(..., gt=0, title="Id пользователя")
    username: str = Field(..., title="Никнейм пользователя")
    first_name: str = Field(..., title="Имя пользователя")
    last_name: str = Field(..., title="Фамилия пользователя")

    model_config = ConfigDict(from_attributes=True)

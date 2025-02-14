from pydantic import BaseModel, ConfigDict, Field


class UserSerializer(BaseModel):
    id: int = Field(..., gt=0, title="Id пользователя")
    name: str = Field(...,  title="Имя пользователя")
    second_name: int = Field(..., title="Фамилия пользователя")

    model_config = ConfigDict(from_attributes=True)


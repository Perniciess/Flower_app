from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")
    role: str = Field(..., description="Роль пользователя")

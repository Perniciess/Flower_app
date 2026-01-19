from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .model import Role


class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")
    role: Role


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, description="Электронная почта пользователя")
    name: str | None = Field(default=None, min_length=1, max_length=64, description="Имя пользователя")
    role: Role | None = None

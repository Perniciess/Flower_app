from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .model import Role


class UserBase(BaseModel):
    """Базовые поля пользователя, используемые в других схемах"""

    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")


class UserCreate(UserBase):
    """Схема для создания пользователя"""

    password: str = Field(..., min_length=8, description="Пароль пользователя")


class UserResponse(UserBase):
    """Схема ответа API с данными пользователя"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")


class UserUpdate(BaseModel):
    """Схема для частичного обновления пользователя"""

    email: EmailStr | None = Field(default=None, description="Электронная почта пользователя")
    name: str | None = Field(default=None, min_length=1, max_length=64, description="Имя пользователя")
    role: Role | None = Field(default=None, description="Роль пользователя")

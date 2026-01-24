from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from .model import Role


class UserBase(BaseModel):
    """Базовые поля пользователя, используемые в других схемах."""

    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        s = str(v)
        if s.startswith("tel:"):
            s = s[4:]
        s = s.replace(" ", "").replace("-", "")

        return s


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str = Field(..., min_length=8, description="Пароль пользователя")


class UserResponse(UserBase):
    """Схема ответа API с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")


class UserUpdate(BaseModel):
    """Схема для частичного обновления пользователя."""

    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")
    name: str | None = Field(default=None, min_length=1, max_length=64, description="Имя пользователя")
    role: Role | None = Field(default=None, description="Роль пользователя")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        s = str(v)
        if s.startswith("tel:"):
            s = s[4:]
        s = s.replace(" ", "").replace("-", "")

        return s

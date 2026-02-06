from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.models.users_model import Role
from app.utils.validators.password import password_strip_and_validate
from app.utils.validators.phone import normalize_phone


class UserBase(BaseModel):
    """Базовые поля пользователя, используемые в других схемах."""

    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str = Field(
        ..., min_length=8, max_length=128, description="Пароль пользователя"
    )


class UserResponse(UserBase):
    """Схема для ответа API с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    role: Role = Field(..., description="Роль пользователя")


class UserUpdate(BaseModel):
    """Схема для частичного обновления пользователя."""

    phone_number: PhoneNumber | None = Field(
        default=None, description="Номер телефона пользователя"
    )
    name: str | None = Field(
        default=None, min_length=1, max_length=64, description="Имя пользователя"
    )
    role: Role | None = Field(default=None, description="Роль пользователя")
    password: str | None = Field(
        default=None, min_length=8, description="Пароль пользователя"
    )

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)

    @field_validator("password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        return password_strip_and_validate(v)

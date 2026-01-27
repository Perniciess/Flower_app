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
    """Схема для ответа API с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")


class UserUpdate(BaseModel):
    """Схема для частичного обновления пользователя."""

    phone_number: PhoneNumber | None = Field(default=None, description="Номер телефона пользователя")
    name: str | None = Field(default=None, min_length=1, max_length=64, description="Имя пользователя")
    role: Role | None = Field(default=None, description="Роль пользователя")
    password: str | None = Field(default=None, min_length=8, description="Пароль пользователя")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        s = str(v)
        if s.startswith("tel:"):
            s = s[4:]
        s = s.replace(" ", "").replace("-", "")

        return s

    @field_validator("password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        v = v.strip()

        if len(v) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов")

        if not any(c.isdigit() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(c.islower() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not any(c.isupper() for c in v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")

        return v

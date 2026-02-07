from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.core.config import settings
from app.schemas.users_schema import UserCreate
from app.utils.validators.password import password_strip_and_validate
from app.utils.validators.phone import normalize_phone


class AuthLogin(BaseModel):
    """Схема для авторизации пользователя."""

    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")
    password: str = Field(..., min_length=8, max_length=128, description="Пароль")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)

    @field_validator("password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        return password_strip_and_validate(v)


class AuthRegister(UserCreate):
    """Схема для регистрации пользователя."""

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)

    @field_validator("name", mode="before")
    @classmethod
    def name_strip(cls, v: str) -> str:
        return v.strip()

    @field_validator("password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        return password_strip_and_validate(v)


class AuthChangePassword(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=128, description="Старый пароль")
    new_password: str = Field(..., min_length=8, max_length=128, description="Новый пароль")

    @field_validator("old_password", "new_password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        return password_strip_and_validate(v)


class AuthSetNewPassword(BaseModel):
    reset_token: str = Field(..., description="Токен сброса пароля")
    new_password: str = Field(..., min_length=8, max_length=128, description="Новый пароль")

    @field_validator("new_password", mode="before")
    @classmethod
    def password_strip_and_validate(cls, v: str) -> str:
        return password_strip_and_validate(v)


class AuthPhone(BaseModel):
    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        return normalize_phone(v)


class VerificationDeepLink(BaseModel):
    token: str = Field(..., description="Токен подтверждения сброса пароля")
    telegram_link: str = Field(..., description="Deeplink telegram")
    expires_in: int = Field(
        default=settings.VERIFICATION_TOKEN_EXPIRY_SECONDS,
        description="Срок истечения кода в секундах",
    )


class AccessToken(BaseModel):
    """Схема для access token."""

    access_token: str = Field(..., description="JWT access токен")


class RefreshToken(BaseModel):
    """Схема для refresh token."""

    refresh_token: str = Field(..., description="JWT refresh токен")


class Tokens(BaseModel):
    """Схема для пары токенов."""

    access_token: str = Field(..., description="JWT access токен")
    refresh_token: str = Field(..., description="JWT refresh токен")


class TokenData(BaseModel):
    """Схема для данных, закодированных в токене."""

    id: str = Field(..., description="ID пользователя")

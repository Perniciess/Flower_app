from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.modules.users.schema import UserCreate


class AuthLogin(BaseModel):
    "Схема для авторизации пользователя."

    phone_number: PhoneNumber = Field(..., description="Номер телефона пользователя")
    password: str = Field(..., min_length=8, description="Пароль")

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
    def password_strip(cls, v: str) -> str:
        return v.strip()


class AuthRegister(UserCreate):
    "Схема для регистрации пользователя."

    @field_validator("phone_number")
    @classmethod
    def normalize_phone(cls, v: PhoneNumber) -> str:
        s = str(v)
        if s.startswith("tel:"):
            s = s[4:]
        s = s.replace(" ", "").replace("-", "")

        return s

    @field_validator("name", mode="before")
    @classmethod
    def name_strip(cls, v: str) -> str:
        return v.strip()

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


class RegisterResponse(BaseModel):
    verification_token: str = Field(..., min_length=8, max_length=8, description="Токен подтверждения номера")
    telegram_link: str = Field(..., description="Deeplink telegram")
    expires_in: int = Field(..., ge=300, le=300, description="Срок истечения кода в секундах")


class AccessToken(BaseModel):
    "Схема access token."

    access_token: str = Field(..., description="JWT access токен")


class RefreshToken(BaseModel):
    "Схема refresh token."

    refresh_token: str = Field(..., description="JWT refresh токен")


class Tokens(BaseModel):
    "Схема пары токенов."

    access_token: str = Field(..., description="JWT access токен")
    refresh_token: str = Field(..., description="JWT refresh токен")
    token_type: str = Field(default="bearer", description="Тип токена")


class TokenData(BaseModel):
    "Данные, закодированные в токене."

    id: str = Field(..., description="ID пользователя")

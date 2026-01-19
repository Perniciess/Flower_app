from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")

    @field_validator("password", mode="before")
    @classmethod
    def password_strip(cls, v: str) -> str:
        return v.strip()


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")

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


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    id: str

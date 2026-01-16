from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")

    @field_validator("password")
    @classmethod
    def password_validation(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.islower() for char in v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not any(char.isupper() for char in v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(not char.isalnum() for char in v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return v

    @field_validator("name", mode="before")
    @classmethod
    def name_strip(cls, v: str) -> str:
        return v.strip()

    @field_validator("password", mode="before")
    @classmethod
    def password_strip(cls, v: str) -> str:
        return v.strip()


class UserOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    name: str = Field(..., min_length=1, max_length=64, description="Имя пользователя")
    role: str = Field(..., description="Роль пользователя")

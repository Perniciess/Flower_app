from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    CSRF_SECRET_KEY: str
    CSRF_COOKIE_NAME: str = "csrftoken"
    CSRF_HEADER_NAME: str = "x-csrftoken"

    ALGORITHM: str = "HS256"

    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "strict"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    # SECURITY.PY
    REFRESH_TOKEN_BYTES: int = 64
    VERIFICATION_TOKEN_LENGTH: int = 8  # если изменить на больше, то нужно  менять схему RegisterResponse
    VERIFICATION_ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # IMAGE PATH
    UPLOAD_DIR: Path = Path("app/static/uploads/flowers")
    ROOT_DIR: Path = Path("app")

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]

    PROJECT_NAME: str

    # POSTGRESQL DATABASE
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    # REDIS DATABASE
    REDIS_URL: str

    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET_KEY: str
    ORDER_EXPIRATION_MINUTES: int = 30
    CAPTURE: bool = True  # True - автосписание, False - после подтверждения. Обговорить с Сашей

    @computed_field
    @property
    def PAYMENT_RETURN_URL(self) -> str:
        return f"{self.FRONTEND_HOST}/orders/payment-result"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore

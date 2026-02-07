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
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    VERIFICATION_TOKEN_EXPIRY_SECONDS: int = 300  # seconds
    CSRF_SECRET_KEY: str
    CSRF_COOKIE_NAME: str = "csrftoken"
    CSRF_HEADER_NAME: str = "x-csrftoken"

    ALGORITHM: str = "HS256"

    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "strict"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    TRUSTED_PROXIES: list[str] = []

    # SECURITY.PY
    REFRESH_TOKEN_BYTES: int = 64
    VERIFICATION_TOKEN_BYTES: int = 16

    # IMAGE PATH
    STATIC_FILES_DIR: str = "static/uploads"

    @computed_field
    @property
    def PRODUCT_UPLOAD_DIR(self) -> Path:
        return Path(self.STATIC_FILES_DIR) / "products"

    @computed_field
    @property
    def CATEGORY_UPLOAD_DIR(self) -> Path:
        return Path(self.STATIC_FILES_DIR) / "categories"

    @computed_field
    @property
    def BANNER_UPLOAD_DIR(self) -> Path:
        return Path(self.STATIC_FILES_DIR) / "banners"

    @computed_field
    @property
    def ROOT_DIR(self) -> Path:
        return Path(self.STATIC_FILES_DIR)

    def get_product_image_url(self, filename: str) -> str:
        """Генерирует URL для изображения продукта."""
        return f"/{self.STATIC_FILES_DIR}/products/{filename}"

    def get_category_image_url(self, filename: str) -> str:
        return f"/{self.STATIC_FILES_DIR}/categories/{filename}"

    def get_banner_image_url(self, filename: str) -> str:
        return f"/{self.STATIC_FILES_DIR}/banners/{filename}"

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
    # ЮKASSA
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET_KEY: str
    ORDER_EXPIRATION_MINUTES: int = 30
    CAPTURE: bool = True  # True - автосписание, False - после подтверждения. Обговорить с Сашей

    # TG URL
    VERIFICATION: str = "https://t.me/kupibuket74_bot?start="
    RESET: str = "https://t.me/kupibuket74_bot?start=reset_"

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

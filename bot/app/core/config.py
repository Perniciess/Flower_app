from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    BOT_TOKEN: str
    BOT_API_KEY: str
    REDIS_URL: str
    BACKEND_URL: str
    WEBSITE_URL: str
    API_V1_STR: str = "/api/v1"
    REGISTER: str = "/auth/complete-register/"
    COMPLETE_RESET: str = "/auth/complete-reset-verification/"


settings = Settings()  # type: ignore

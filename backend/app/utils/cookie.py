from typing import Literal, TypedDict

from fastapi import Response

from app.core.config import settings
from app.schemas.auth_schema import Tokens


class CookieSettings(TypedDict):
    key: str
    secure: bool
    samesite: Literal["lax", "strict", "none"]


def get_refresh_cookie_settings() -> CookieSettings:
    """
    Возвращает имя ключа и настройки безопасности
    в зависимости от того, используем ли мы HTTPS.
    """
    if settings.COOKIE_SECURE:
        return {
            "key": "__Host-rt",
            "secure": True,
            "samesite": "lax",
        }
    else:
        return {
            "key": "rt",
            "secure": False,
            "samesite": "lax",
        }


def set_token(response: Response, tokens: Tokens) -> None:
    """Устанавливаем refresh токен в cookie."""
    cookie_params = get_refresh_cookie_settings()

    response.set_cookie(
        key=cookie_params["key"],
        value=tokens.refresh_token,
        httponly=True,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )


def remove_token(response: Response) -> None:
    """Удаляем refresh токен из cookie."""
    cookie_params = get_refresh_cookie_settings()

    response.delete_cookie(
        key=cookie_params["key"],
        httponly=True,
        secure=cookie_params["secure"],
        samesite=cookie_params["samesite"],
        path="/",
    )

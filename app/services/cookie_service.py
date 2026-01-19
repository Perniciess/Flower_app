from fastapi import Response

from app.core.config import settings
from app.schemas.auth_schemas import Tokens


def set_token(response: Response, tokens: Tokens) -> None:
    response.set_cookie(
        key="access_token",
        value=f"{tokens.token_type} {tokens.access_token}",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def remove_token(response: Response) -> None:
    response.delete_cookie(
        key="access_token",
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )

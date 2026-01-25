import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pwdlib import PasswordHash

from .config import settings

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(*, user_id: int) -> str:
    """
    Создание access токена

    Args:
        user_id: идентификатор пользователя

    Returns:
        str: access токен
    """
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def get_refresh_hash(refresh_token: str) -> str:
    return hmac.new(settings.SECRET_KEY.encode(), refresh_token.encode(), hashlib.sha256).hexdigest()


def get_expires_at_refresh_token() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


def generate_verification_token() -> str:
    """Генерация кода верификации для Telegram."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(8))

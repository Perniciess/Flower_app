import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from redis.asyncio import Redis

from .config import settings

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сверка полученного пароля с хешированным из БД."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Получение хеша пароля argon2."""
    return password_hash.hash(password)


def create_access_token(*, user_id: int) -> str:
    """Создание access токена."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token() -> str:
    """Создание refresh токена"""
    return secrets.token_urlsafe(settings.REFRESH_TOKEN_BYTES)


def get_refresh_hash(refresh_token: str) -> str:
    """Получение хеша refresh токена."""
    return hashlib.sha256(refresh_token.encode()).hexdigest()


def get_expires_at_refresh_token() -> datetime:
    """Создание времени жизни refresh токена."""
    return datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


def generate_verification_token() -> str:
    """Генерация токена верификации для Telegram."""
    return secrets.token_urlsafe(settings.VERIFICATION_TOKEN_BYTES)


async def add_to_blacklist(redis: Redis, access_token: str) -> None:
    """Добавить токен в blacklist до его истечения."""
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        exp = payload.get("exp")
        if exp:
            expires_in = exp - int(datetime.now(tz=UTC).timestamp())
            if expires_in > 0:
                token_hash = hashlib.sha256(access_token.encode()).hexdigest()
                await redis.set(f"bl:{token_hash}", "1", ex=expires_in)
    except jwt.InvalidTokenError:
        pass


async def is_blacklisted(redis: Redis, token: str) -> bool:
    """Проверить, находится ли токен в blacklist."""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return await redis.exists(f"bl:{token_hash}") > 0


async def get_content_hash(content: bytes, algorithm: str = "md5") -> str:
    return hashlib.new(algorithm, content).hexdigest()

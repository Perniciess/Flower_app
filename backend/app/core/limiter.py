from typing import Any, cast

from fastapi import Request
from limits.storage import RedisStorage
from slowapi import Limiter

from app.core.config import settings


def real_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


_storage: RedisStorage | None = None

limiter = Limiter(key_func=real_ip)


def init_limiter() -> None:
    global _storage

    _storage = RedisStorage(
        settings.REDIS_URL,
        socket_timeout=2,
        socket_connect_timeout=2,
    )

    cast(Any, limiter).storage = _storage

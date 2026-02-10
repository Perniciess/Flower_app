from typing import Any, cast

from fastapi import Request
from limits.storage import RedisStorage
from slowapi import Limiter

from app.core.config import settings


def real_ip(request: Request) -> str:
    """Extract real client IP for rate limiting.

    Only trusts X-Forwarded-For header if request comes from a trusted proxy.
    If TRUSTED_PROXIES is empty, always uses request.client.host (safe default).

    Args:
        request: FastAPI request object

    Returns:
        Client IP address string
    """
    # Safe default: if no trusted proxies configured, use direct client IP
    if not settings.TRUSTED_PROXIES:
        if request.client:
            return request.client.host
        return "unknown"

    # Only trust X-Forwarded-For if request comes from a known proxy
    if request.client and request.client.host in settings.TRUSTED_PROXIES:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()

    # Fallback to direct client IP
    if request.client:
        return request.client.host

    return "unknown"


_storage: RedisStorage | None = None

limiter = Limiter(key_func=real_ip, default_limits=["60/minute"])


def init_limiter() -> None:
    global _storage

    _storage = RedisStorage(
        settings.REDIS_URL,
        socket_timeout=2,
        socket_connect_timeout=2,
    )

    cast(Any, limiter).storage = _storage

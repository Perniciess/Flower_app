"""Rate limiting configuration using slowapi."""

from slowapi import Limiter
from slowapi.util import get_remote_address


def get_limiter() -> Limiter:
    """
    Создает и возвращает настроенный rate limiter.

    Returns:
        Limiter: Настроенный экземпляр slowapi Limiter
    """
    return Limiter(
        key_func=get_remote_address,
        default_limits=["200/minute"],  # Глобальный лимит по умолчанию
        storage_uri="memory://",  # Можно заменить на Redis для distributed setup
    )


# Глобальный экземпляр limiter
limiter = get_limiter()

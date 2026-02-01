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
        storage_uri="memory://",
    )


limiter = get_limiter()

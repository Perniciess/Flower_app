from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import settings


def get_limiter() -> Limiter:
    return Limiter(
        key_func=get_remote_address,
        storage_uri=settings.REDIS_URL,
    )


limiter = get_limiter()

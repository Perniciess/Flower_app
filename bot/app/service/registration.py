import json

import httpx

from app.core.config import settings
from app.core.redis import redis_manager


async def check_cache(token: str) -> bool:
    redis = redis_manager.get_client()
    value = await redis.get(f"v:{token}")
    if not value:
        return False
    return True


async def verify_account(token: str, phone_number: str) -> bool:
    redis = redis_manager.get_client()
    value = await redis.get(f"v:{token}")
    if not value:
        return False
    user_data = json.loads(value)
    return phone_number == user_data["phone_number"]


async def complete_verify(token: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.BACKEND_URL}{settings.API_V1_STR}/auth/complete-register/{token}",
                timeout=10.0,
            )
            return response.is_success
    except httpx.RequestError:
        return False

import json

import httpx
from redis.asyncio import Redis

from app.core.config import settings

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def check_cache(token: str) -> bool:
    value = await redis.get(f"verification:{token}")
    if not value:
        return False
    return True


async def verify_account(token: str, phone_number: str) -> bool:
    value = await redis.get(f"verification:{token}")
    if not value:
        return False
    user_data = json.loads(value)
    return phone_number == user_data["phone_number"]


async def complete_verify(token: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.BACKEND_URL}/auth/complete-register/{token}",
                timeout=10.0,
            )
            return response.is_success
    except httpx.RequestError:
        return False

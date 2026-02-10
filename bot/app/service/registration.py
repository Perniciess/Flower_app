import json

import httpx

from app.core.config import settings
from app.core.redis import redis_manager


async def check_token(token: str, type: str) -> bool:
    redis = redis_manager.get_client()
    value = await redis.get(f"{type}:{token}")
    return value is not None


async def verify(token: str, type: str, phone_number: str) -> bool:
    redis = redis_manager.get_client()
    value = await redis.get(f"{type}:{token}")
    if not value:
        return False
    user_data = json.loads(value)
    return phone_number == user_data["phone_number"]


async def complete(token: str, url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.BACKEND_URL}{settings.API_V1_STR}{url}{token}",
                headers={"X-Bot-Api-Key": settings.BOT_API_KEY},
                timeout=10.0,
            )
            return response.is_success
    except httpx.RequestError:
        return False

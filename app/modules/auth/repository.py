from collections.abc import Mapping
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from .model import RefreshToken


async def create_refresh_token(*, session: AsyncSession, data: Mapping[str, Any]) -> RefreshToken:
    refresh = RefreshToken(
        user_id=data["user_id"],
        token_hash=data["token_hash"],
        expires_at=data["expires_at"],
        last_used_at=None,
        is_revoked=False,
    )
    session.add(refresh)
    await session.commit()
    await session.refresh(refresh)
    return refresh

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_model import RefreshToken


def _create_refresh_token_instance(data: Mapping[str, Any]) -> RefreshToken:
    return RefreshToken(
        user_id=data["user_id"],
        token_hash=data["token_hash"],
        expires_at=data["expires_at"],
        last_used_at=None,
        is_revoked=False,
    )


async def create_refresh_token(*, session: AsyncSession, data: Mapping[str, Any]) -> RefreshToken:
    refresh = _create_refresh_token_instance(data)
    session.add(refresh)
    await session.flush()
    return refresh


async def get_refresh_token(*, session: AsyncSession, token_hash: str) -> RefreshToken | None:
    statement = (
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .where(RefreshToken.is_revoked.is_(False))
        .where(RefreshToken.expires_at > datetime.now(UTC))
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_refresh_token_for_update(*, session: AsyncSession, token_hash: str) -> RefreshToken | None:
    statement = (
        select(RefreshToken)
        .where(RefreshToken.token_hash == token_hash)
        .where(RefreshToken.is_revoked.is_(False))
        .where(RefreshToken.expires_at > datetime.now(UTC))
        .with_for_update()
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def revoke_token(*, session: AsyncSession, token_id: int) -> bool:
    now = datetime.now(UTC)
    statement = (
        update(RefreshToken)
        .where(RefreshToken.id == token_id)
        .where(RefreshToken.expires_at > now)
        .where(RefreshToken.is_revoked.is_(False))
        .values(last_used_at=now, is_revoked=True)
        .returning(RefreshToken.id)
    )
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none() is not None


async def revoke_all(*, session: AsyncSession, user_id: int) -> bool:
    statement = (
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .where(RefreshToken.is_revoked.is_(False))
        .values(is_revoked=True)
        .returning(RefreshToken.id)
    )
    result = await session.execute(statement)
    await session.flush()
    return len(result.scalars().all()) > 0


async def delete_expired_tokens(*, session: AsyncSession) -> int:
    """Удаляет истекшие и отозванные refresh токены.

    Args:
        session: Асинхронная сессия БД

    Returns:
        Количество удаленных токенов
    """
    from sqlalchemy import delete, or_

    now = datetime.now(UTC)
    statement = (
        delete(RefreshToken)
        .where(
            or_(
                RefreshToken.expires_at < now,
                RefreshToken.is_revoked.is_(True),
            )
        )
        .returning(RefreshToken.id)
    )
    result = await session.execute(statement)
    return len(result.scalars().all())

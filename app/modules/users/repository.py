from collections.abc import Mapping, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User


async def create_user(*, session: AsyncSession, data: Mapping[str, str]) -> User:
    user = User(
        email=data["email"],
        name=data["name"],
        password_hash=data["password_hash"],
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = await session.execute(statement)
    return user.scalar_one_or_none()


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    user = await session.execute(statement)
    return user.scalar_one_or_none()


async def update_user(*, session: AsyncSession, user_id: int, data: Mapping[str, object]) -> User | None:
    statement = update(User).where(User.id == user_id).values(**data).returning(User)
    result = await session.execute(statement)
    user: User | None = result.scalar_one_or_none()
    if user is None:
        await session.rollback()
        return None
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(*, session: AsyncSession) -> Sequence[User]:
    statement = select(User).order_by(User.id)
    users = await session.execute(statement)
    return users.scalars().all()

from collections.abc import Mapping

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users_model import User


async def create_user(*, session: AsyncSession, data: Mapping[str, str]) -> User:
    user = User(
        phone_number=data["phone_number"],
        name=data["name"],
        password_hash=data["password_hash"],
    )
    session.add(user)
    await session.flush()
    return user


async def get_user_by_phone(*, session: AsyncSession, phone_number: str) -> User | None:
    statement = select(User).where(User.phone_number == phone_number)
    user = await session.execute(statement)
    return user.scalar_one_or_none()


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    user = await session.execute(statement)
    return user.scalar_one_or_none()


async def update_user(*, session: AsyncSession, user_id: int, data: Mapping[str, object]) -> User | None:
    statement = update(User).where(User.id == user_id).values(**data).returning(User)
    result = await session.execute(statement)
    await session.flush()
    return result.scalar_one_or_none()


async def get_users():
    return select(User).order_by(User.id)

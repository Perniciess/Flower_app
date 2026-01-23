from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash

from . import repository as user_repository
from .schema import UserCreate, UserResponse, UserUpdate


async def create_user(*, session: AsyncSession, data: UserCreate) -> UserResponse:
    """
    Создает нового пользователя в базе данных

    Args:
        session: сессия базы данных

    """
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "password_hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserResponse.model_validate(new_user)


async def get_user_by_email(*, session: AsyncSession, email: str) -> UserResponse:
    user = await user_repository.get_user_by_email(session=session, email=email)
    if user is None:
        raise UserNotFoundError(email=email)

    return UserResponse.model_validate(user)


async def update_user(*, session: AsyncSession, user_id: int, data: UserUpdate) -> UserResponse:
    patch = data.model_dump(exclude_unset=True)
    user = await user_repository.update_user(session=session, user_id=user_id, data=patch)
    if user is None:
        raise UserNotFoundError(user_id=user_id)
    return UserResponse.model_validate(user)


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> UserResponse:
    user = await user_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id=user_id)

    return UserResponse.model_validate(user)


async def get_users(*, session: AsyncSession) -> Sequence[UserResponse]:
    users = await user_repository.get_users(session=session)
    return [UserResponse.model_validate(u) for u in users]

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash
from app.repository import users_repository
from app.schemas.users_schema import UserCreate, UserResponse, UserUpdate


async def create_user(*, session: AsyncSession, data: UserCreate) -> UserResponse:
    """
    Создает нового пользователя в базе данных.

    Args:
        session: сессия базы данных
        data: данные для создания пользователя

    Returns:
        UserResponse с данными созданного пользователя

    Raises:
        UserAlreadyExistsError: если пользователь с таким phone_number уже существует
    """
    user_exist = await users_repository.get_user_by_phone(session=session, phone_number=data.phone_number)
    if user_exist:
        raise UserAlreadyExistsError(data.phone_number)

    data_user = {
        "phone_number": data.phone_number,
        "name": data.name,
        "password_hash": get_password_hash(data.password),
    }

    new_user = await users_repository.create_user(session=session, data=data_user)
    return UserResponse.model_validate(new_user)


async def get_user_by_phone(*, session: AsyncSession, phone_number: str) -> UserResponse:
    """
    Возвращает пользователя по его номеру телефона.

    Args:
        session: сессия базы данных
        phone_number: номер телефона пользователя

    Returns:
        UserResponse с данными созданного пользователя

    Raises:
        UserNotFoundError: если пользователь с таким номером не найден
    """
    user = await users_repository.get_user_by_phone(session=session, phone_number=phone_number)
    if user is None:
        raise UserNotFoundError(phone_number=phone_number)

    return UserResponse.model_validate(user)


async def update_user(*, session: AsyncSession, user_id: int, data: UserUpdate) -> UserResponse:
    """
    Обновляет данные пользователя.

    Args:
        session: сессия базы данных
        user_id: идентификтаор пользователя
        data: новые данные пользователя

    Returns:
        UserResponse с данными созданного пользователя

    Raises:
        UserNotFoundError: если пользователь с таким phone_number не найден
    """
    patch = data.model_dump(exclude_unset=True)
    password = patch.pop("password", None)
    if password:
        patch["password_hash"] = get_password_hash(password)

    user = await users_repository.update_user(session=session, user_id=user_id, data=patch)
    if user is None:
        raise UserNotFoundError(user_id=user_id)
    return UserResponse.model_validate(user)


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> UserResponse:
    """
    Возвращает пользователя по идентификатору.

    Args:
        session: сессия базы данных
        user_id: идентификтаор пользователя

    Returns:
        UserResponse с данными созданного пользователя

    Raises:
        UserNotFoundError: если пользователь с таким phone_number не найден
    """
    user = await users_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id=user_id)

    return UserResponse.model_validate(user)


async def get_users(*, session: AsyncSession) -> Page[UserResponse]:
    """
    Возвращает пагинированный список пользователей.

    Args:
        session: сессия базы данных

    Returns:
        Page[UserResponse] список пользователей

    """
    users = await users_repository.get_users()
    return await paginate(session, users)

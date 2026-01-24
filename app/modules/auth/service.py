from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidToken, PasswordsDoNotMatchError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_expires_at_refresh_token,
    get_password_hash,
    get_refresh_hash,
    verify_password,
)
from app.modules.users import repository as user_repository
from app.modules.users.schema import UserResponse

from . import repository as auth_repository
from .schema import AuthLogin, AuthRegister, Tokens


async def register(*, session: AsyncSession, data: AuthRegister) -> UserResponse:
    """
    Регистрирует нового пользователя в базе данных.

    Args:
        session: сессия базы данных
        data: данные для создания пользователя

    Returns:
        UserResponse с данными созданного пользователя

    Raises:
        UserAlreadyExistsError: если пользователь с таким phone_number уже существует
    """
    user_exist = await user_repository.get_user_by_phone(session=session, phone_number=data.phone_number)
    if user_exist:
        raise UserAlreadyExistsError(data.phone_number)

    data_user = {"phone_number": data.phone_number, "name": data.name, "password_hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserResponse.model_validate(new_user)


async def login(*, session: AsyncSession, data: AuthLogin) -> Tokens:
    """
    Авторизует пользователя в системе.

    Args:
        session: сессия базы данных
        data: данные для авторизации пользователя

    Returns:
        Tokens: access и refresh токены

    Raises:
        UserNotFoundError: если пользователь с таким phone_number уже существует
        PasswordsDoNotMatchError: если пароли не совпадают
    """
    user = await user_repository.get_user_by_phone(session=session, phone_number=data.phone_number)
    if user is None:
        raise UserNotFoundError(phone_number=data.phone_number)

    if not verify_password(data.password, user.password_hash):
        raise PasswordsDoNotMatchError()

    access_token = create_access_token(user_id=user.id)
    refresh_token = await _save_refresh_token(session=session, user_id=user.id)

    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


async def logout(*, session: AsyncSession, refresh_token: str) -> None:
    """
    Выход пользователя из системы

    Args:
        session: сессия базы данных
        refresh_token: переданный refresh токен

    Returns:
        None

    Raises:
        InvalidToken: если переданный refresh токен не соответствует токену в БД
    """
    refresh_hash = get_refresh_hash(refresh_token)

    token = await auth_repository.get_refresh_token(session=session, token_hash=refresh_hash)
    if token is None:
        raise InvalidToken()

    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidToken()


async def refresh_tokens(*, session: AsyncSession, refresh_token: str) -> Tokens:
    """
    Обновление токенов

    Args:
        session: сессия базы данных
        refresh_token: переданный refresh токен

    Returns:
        Tokens: access и refresh токены

    Raises:
        InvalidToken: если переданный refresh токен не соответствует токену в БД
    """
    refresh_hash = get_refresh_hash(refresh_token)

    token = await auth_repository.get_refresh_token_for_update(session=session, token_hash=refresh_hash)
    if token is None:
        raise InvalidToken()

    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidToken()

    access_token = create_access_token(user_id=token.user_id)
    new_refresh_token = await _save_refresh_token(session=session, user_id=token.user_id)

    return Tokens(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")


async def _save_refresh_token(*, session: AsyncSession, user_id: int) -> str:
    """
    Cохранение refresh токена

    Args:
        session: сессия базы данных
        user_id: идентификатор пользователя

    Returns:
        str: refresh токен
    """
    refresh_token = create_refresh_token()
    refresh_hash = get_refresh_hash(refresh_token)
    expires_at = get_expires_at_refresh_token()

    token_data = {
        "user_id": user_id,
        "token_hash": refresh_hash,
        "expires_at": expires_at,
    }

    await auth_repository.create_refresh_token(session=session, data=token_data)
    return refresh_token

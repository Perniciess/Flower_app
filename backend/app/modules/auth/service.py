import json
from typing import Any

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenError,
    PasswordsDoNotMatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserNotUpdatedError,
)
from app.core.security import (
    add_to_blacklist,
    create_access_token,
    create_refresh_token,
    generate_verification_token,
    get_expires_at_refresh_token,
    get_password_hash,
    get_refresh_hash,
    verify_password,
)
from app.modules.users import repository as user_repository

from . import repository as auth_repository
from .schema import AuthChangePassword, AuthLogin, AuthRegister, Tokens, VerificationDeepLink


async def register(*, session: AsyncSession, redis: Redis, data: AuthRegister) -> VerificationDeepLink:
    """
    Начальная регистрация с генерацией deeplink для подтверждения номера в телеграме и проверке через Redis.

    Args:
        session: сессия базы данных
        redis: сессия Redis
        data: данные для регистрации пользователя

    Returns:
        RegisterResponse данные для продолжения верификации

    Raises:
        UserAlreadyExistsError: если пользователь с таким phone_number уже существует
    """
    user_exist = await user_repository.get_user_by_phone(session=session, phone_number=data.phone_number)
    if user_exist:
        raise UserAlreadyExistsError(data.phone_number)

    verification_token = generate_verification_token()
    data_user = {
        "phone_number": data.phone_number,
        "name": data.name,
        "password_hash": get_password_hash(data.password),
        "verification_token": verification_token,
    }
    await redis.set(f"v:{verification_token}", json.dumps(data_user), ex=300)
    telegram_link = f"{settings.VERIFICATION}{verification_token}"
    return VerificationDeepLink(token=data_user["verification_token"], telegram_link=telegram_link, expires_in=300)


async def complete_register(*, session: AsyncSession, redis: Redis, verification_token: str) -> None:
    """
    Конец регистрации пользователя, после подтверждения номера в телеграме.

    Args:
        session: сессия базы данных
        redis: сессия Redis
        verification_token: токен проверки пользователя

    Returns:
        None

    Raises:
        InvalidTokenError: неправильный токен
    """
    data_user = await _get_redis_data(redis, f"v:{verification_token}")

    await user_repository.create_user(session=session, data=data_user)
    await redis.delete(f"v:{verification_token}")


async def login(*, session: AsyncSession, data: AuthLogin) -> Tokens:
    """
    Авторизует пользователя в системе.

    Args:
        session: сессия базы данных
        data: данные для авторизации пользователя

    Returns:
        Tokens: access и refresh токены

    Raises:
        UserNotFoundError: если пользователь с таким phone_number не существует
        PasswordsDoNotMatchError: если пароли не совпадают
    """
    user = await user_repository.get_user_by_phone(session=session, phone_number=data.phone_number)
    if user is None:
        raise UserNotFoundError(phone_number=data.phone_number)

    if not verify_password(data.password, user.password_hash):
        raise PasswordsDoNotMatchError()

    access_token = create_access_token(user_id=user.id)
    refresh_token = await _save_refresh_token(session=session, user_id=user.id)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


async def logout(*, session: AsyncSession, redis: Redis, access_token: str, refresh_token: str) -> None:
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
        raise InvalidTokenError()
    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidTokenError()

    await add_to_blacklist(redis=redis, access_token=access_token)


async def refresh_tokens(*, session: AsyncSession, refresh_token: str) -> Tokens:
    """
    Обновляет токены

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
    if token is None or token.is_revoked:
        raise InvalidTokenError()

    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidTokenError()

    access_token = create_access_token(user_id=token.user_id)
    new_refresh_token = await _save_refresh_token(session=session, user_id=token.user_id)

    return Tokens(access_token=access_token, refresh_token=new_refresh_token)


async def change_password(
    *, session: AsyncSession, redis: Redis, access_token: str, user_id: int, data: AuthChangePassword
) -> Tokens:
    """
    Изменяет пароль пользователя

    Args:
        session: сессия базы данных
        redis: сессия redis хранилища
        access_token: переданный refresh токен
        user_id: идентификатор пользователя
        data: пароли

    Returns:
        Tokens: access и refresh токены

    Raises:
        UserNotUpdatedError: если пользователь передал 2 одинаковых пароля
        UserNotFoundError: если пользователь не найден
        PasswordsDoNotMatchError: если переданный старый пароль и пароль из БД не совпадают
        InvalidToken: если переданный refresh токен не соответствует токену в БД
    """
    if data.old_password == data.new_password:
        raise UserNotUpdatedError(user_id=user_id)

    user = await user_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id=user_id)

    if not verify_password(data.old_password, user.password_hash):
        raise PasswordsDoNotMatchError("Неверный старый пароль")

    new_password_hash = get_password_hash(data.new_password)
    updated_user = await user_repository.update_user(
        session=session, user_id=user_id, data={"password_hash": new_password_hash}
    )
    if updated_user is None:
        raise UserNotUpdatedError(user_id=user_id)

    revoked = await auth_repository.revoke_all(session=session, user_id=user.id)
    if not revoked:
        raise InvalidTokenError()

    new_access_token = create_access_token(user_id=user.id)
    refresh_token = await _save_refresh_token(session=session, user_id=user.id)
    await add_to_blacklist(redis=redis, access_token=access_token)
    return Tokens(access_token=new_access_token, refresh_token=refresh_token)


async def reset_password(*, session: AsyncSession, redis: Redis, phone_number: str) -> VerificationDeepLink:
    """
    Начинает сброс пароля пользователя

    Args:
        session: сессия базы данных
        redis: сессия redis хранилища
        phone_number: номер телефона пользователя

    Returns:
        VerificationDeepLink: ссылка на ТГ-бота для сброса

    Raises:
        UserNotFoundError: если пользователь не найден
    """
    user_exist = await user_repository.get_user_by_phone(session=session, phone_number=phone_number)
    if not user_exist:
        raise UserNotFoundError(phone_number=phone_number)

    reset_token = generate_verification_token()
    user_data = {
        "user_id": user_exist.id,
        "phone_number": phone_number,
    }
    await redis.set(f"r:{reset_token}", json.dumps(user_data), ex=300)
    telegram_link = f"{settings.RESET}{reset_token}"
    return VerificationDeepLink(token=reset_token, telegram_link=telegram_link, expires_in=300)


async def complete_reset(*, redis: Redis, reset_token: str) -> None:
    """
    Завершает сброс пароля пользователя

    Args:
        session: сессия базы данных
        redis: сессия redis хранилища
        reset_token: токен сброса пароля

    Returns:
        None
    """
    data_user = await _get_redis_data(redis, f"r:{reset_token}")

    ttl = await redis.ttl(f"r:{reset_token}")
    data_user["verified"] = True
    await redis.set(f"r:{reset_token}", json.dumps(data_user), ex=ttl)
    await redis.publish(f"reset:{reset_token}", "verified")


async def set_new_password(*, session: AsyncSession, redis: Redis, reset_token: str, new_password: str) -> Tokens:
    """
    Устанавливает новый пароль

    Args:
        session: сессия базы данных
        redis: сессия redis хранилища
        reset_token: токен сброса пароля
        new_password: новый пароль пользователя

    Returns:
        Tokens: access и refresh токены

    Raises:
        InvalidTokenError: если токен сброса не совпадает с токеном из хранилища
        UserNotUpdatedError: если пользователь не нгайден
    """
    data_user = await _get_redis_data(redis, f"r:{reset_token}")

    if not data_user.get("verified"):
        raise InvalidTokenError()

    user_id = data_user["user_id"]
    new_password_hash = get_password_hash(new_password)
    updated_user = await user_repository.update_user(
        session=session, user_id=user_id, data={"password_hash": new_password_hash}
    )
    if updated_user is None:
        raise UserNotUpdatedError(user_id=user_id)

    await auth_repository.revoke_all(session=session, user_id=user_id)
    await redis.delete(f"r:{reset_token}")

    access_token = create_access_token(user_id=user_id)
    refresh_token = await _save_refresh_token(session=session, user_id=user_id)
    return Tokens(access_token=access_token, refresh_token=refresh_token)


async def _save_refresh_token(*, session: AsyncSession, user_id: int) -> str:
    """
    Cохраняет refresh токен

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


async def _get_redis_data(redis: Redis, key: str) -> dict[str, Any]:
    """
    Получает данные из redis по токену

    Args:
        redis: сессия хранилища redis
        key: токен для подтверждения

    Returns:
        JSON с данными из redis

    Raises:
        InvalidTokenError: по ключу в хранилище ничего не найдено
    """
    raw = await redis.get(key)
    if raw is None:
        raise InvalidTokenError()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        await redis.delete(key)
        raise InvalidTokenError() from None

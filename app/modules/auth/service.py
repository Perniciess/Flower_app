import secrets
from datetime import UTC, datetime, timedelta

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import InvalidToken, PasswordsDoNotMatchError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash, get_refresh_hash, verify_password
from app.modules.users import repository as user_repository
from app.modules.users.schema import UserResponse

from . import repository as auth_repository
from .schema import AuthLogin, AuthRegister, Tokens


async def register(*, session: AsyncSession, data: AuthRegister) -> UserResponse:
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "password_hash": get_password_hash(data.password)}
    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserResponse.model_validate(new_user)


async def login(*, session: AsyncSession, data: AuthLogin) -> Tokens:
    user = await user_repository.get_user_by_email(session=session, email=data.email)
    if user is None:
        raise UserNotFoundError(email=data.email)

    if not verify_password(data.password, user.password_hash):
        raise PasswordsDoNotMatchError()

    access_token = _create_access_token(user_id=user.id)
    refresh_token = await _create_and_save_refresh_token(session=session, user_id=user.id)

    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


async def logout(*, session: AsyncSession, refresh_token: str) -> None:
    refresh_hash = get_refresh_hash(refresh_token)

    token = await auth_repository.get_refresh_token(session=session, token_hash=refresh_hash)
    if token is None:
        raise InvalidToken()

    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidToken()


async def refresh_tokens(*, session: AsyncSession, refresh_token: str) -> Tokens:
    refresh_hash = get_refresh_hash(refresh_token)

    token = await auth_repository.get_refresh_token_for_update(session=session, token_hash=refresh_hash)
    if token is None:
        raise InvalidToken()

    revoked = await auth_repository.revoke_token(session=session, token_id=token.id)
    if not revoked:
        raise InvalidToken()

    access_token = _create_access_token(user_id=token.user_id)
    new_refresh_token = await _create_and_save_refresh_token(session=session, user_id=token.user_id)

    return Tokens(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")


async def _create_and_save_refresh_token(*, session: AsyncSession, user_id: int) -> str:
    refresh_token = secrets.token_urlsafe(64)
    refresh_hash = get_refresh_hash(refresh_token)
    expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    token_data = {
        "user_id": user_id,
        "token_hash": refresh_hash,
        "expires_at": expires_at,
    }

    await auth_repository.create_refresh_token(session=session, data=token_data)
    return refresh_token


def _create_access_token(*, user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

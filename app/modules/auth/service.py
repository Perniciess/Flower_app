import secrets
from datetime import UTC, datetime, timedelta

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import PasswordsDoNotMatchError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash, get_refresh_hash, verify_password
from app.modules.users import repository as user_repository
from app.modules.users.schema import UserOutput

from . import repository as auth_repository
from .schema import Tokens, UserLogin, UserRegister


async def register(*, session: AsyncSession, data: UserRegister) -> UserOutput:
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "password_hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserOutput.model_validate(new_user)


async def login(*, session: AsyncSession, data: UserLogin) -> Tokens:
    user = await user_repository.get_user_by_email(session=session, email=data.email)
    if user is None:
        raise UserNotFoundError(email=data.email)
    if not verify_password(data.password, user.password_hash):
        raise PasswordsDoNotMatchError()

    access_token = _create_access_token(data={"sub": str(user.id)})

    refresh_token = secrets.token_urlsafe(64)
    refresh_hash = get_refresh_hash(refresh_token)

    expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    await auth_repository.create_refresh_token(
        session=session,
        data={
            "user_id": user.id,
            "token_hash": refresh_hash,
            "expires_at": expires_at,
        },
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def _create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

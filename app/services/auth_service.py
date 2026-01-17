from datetime import UTC, datetime, timedelta

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import PasswordsDoNotMatchError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash, verify_password
from app.repositories import user_repository
from app.schemas.auth_schemas import Token, UserLogin, UserRegister
from app.schemas.user_schemas import UserOutput


async def register(*, session: AsyncSession, data: UserRegister) -> UserOutput:
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserOutput.model_validate(new_user)


async def login(*, session: AsyncSession, data: UserLogin) -> Token:
    user = await user_repository.get_user_by_email(session=session, email=data.email)
    if user is None:
        raise UserNotFoundError(email=data.email)
    if not verify_password(data.password, user.hash):
        raise PasswordsDoNotMatchError()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

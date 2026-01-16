from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PasswordsDoNotMatchError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash, verify_password
from app.repositories import user_repository
from app.schemas.auth_schemas import UserLogin, UserRegister
from app.schemas.user_schemas import UserOutput


async def register(*, session: AsyncSession, data: UserRegister) -> UserOutput:
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserOutput.model_validate(new_user)


async def login(*, session: AsyncSession, data: UserLogin) -> UserOutput:
    user = await user_repository.get_user_by_email(session=session, email=data.email)
    if user is None:
        raise UserNotFoundError(email=data.email)
    if not verify_password(data.password, user.hash):
        raise PasswordsDoNotMatchError

    return UserOutput.model_validate(user)

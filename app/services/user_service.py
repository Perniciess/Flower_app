from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import get_password_hash
from app.repositories import user_repository
from app.schemas.user_schemas import UserOutput, UserUpdate


async def create_user(*, session: AsyncSession, data) -> UserOutput:
    user_exist = await user_repository.get_user_by_email(session=session, email=data.email)
    if user_exist:
        raise UserAlreadyExistsError(data.email)

    data_user = {"email": data.email, "name": data.name, "hash": get_password_hash(data.password)}

    new_user = await user_repository.create_user(session=session, data=data_user)
    return UserOutput.model_validate(new_user)


async def get_user_by_email(*, session: AsyncSession, email: str) -> UserOutput:
    user = await user_repository.get_user_by_email(session=session, email=email)
    if user is None:
        raise UserNotFoundError(email=email)

    return UserOutput.model_validate(user)


async def update_user(*, session: AsyncSession, user_id: int, data: UserUpdate) -> UserOutput:
    patch = data.model_dump(exclude_unset=True)
    user = await user_repository.update_user(session=session, user_id=user_id, data=patch)
    if user is None:
        raise UserNotFoundError(user_id=user_id)
    return UserOutput.model_validate(user)


async def get_user_by_id(*, session: AsyncSession, user_id: int) -> UserOutput:
    user = await user_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id=user_id)

    return UserOutput.model_validate(user)


async def get_users(*, session: AsyncSession) -> Sequence[UserOutput]:
    users = await user_repository.get_users(session=session)
    return [UserOutput.model_validate(u) for u in users]

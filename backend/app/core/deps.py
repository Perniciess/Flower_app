import jwt
from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.users import repository as user_repository
from app.modules.users.model import Role, User

from .config import settings
from .exceptions import InsufficientPermissionError, InvalidTokenError
from .redis import get_redis
from .security import is_blacklisted, oauth2_scheme


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    header_token: str | None = Depends(oauth2_scheme),
):
    token = header_token or request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if await is_blacklisted(redis, token):
        raise InvalidTokenError()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        user_id = int(sub)
    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Could not validate credentials") from None

    user = await user_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[Role]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role in self.allowed_roles:
            return current_user

        raise InsufficientPermissionError()


require_admin = RoleChecker([Role.ADMIN])
require_client = RoleChecker([Role.CLIENT, Role.ADMIN])

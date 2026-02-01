import jwt
from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa.domain.common import SecurityHelper

from app.db.session import get_db
from app.models.users_model import Role, User
from app.repository import users_repository

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
    """Получение активного пользователя из токена."""
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

    user = await users_repository.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user


class RoleChecker:
    """RBAC класс, для работы с ролями."""

    def __init__(self, allowed_roles: list[Role]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role in self.allowed_roles:
            return current_user

        raise InsufficientPermissionError()


require_admin = RoleChecker([Role.ADMIN])
require_client = RoleChecker([Role.CLIENT, Role.ADMIN])


async def verify_yookassa_request(request: Request) -> None:
    """
    Зависимость для проверки, что запрос пришел именно от серверов ЮKassa.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")

    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        if request.client is None:
            raise HTTPException(status_code=400, detail="Could not determine client IP")
        client_ip = request.client.host

    try:
        is_trusted = SecurityHelper().is_ip_trusted(client_ip)
    except Exception:
        is_trusted = False

    if not is_trusted:
        raise HTTPException(status_code=403, detail="Forbidden: Untrusted IP source")

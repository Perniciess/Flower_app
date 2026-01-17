import jwt
from fastapi import Depends, HTTPException, Request, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.database.session import get_db
from app.repositories import user_repository


def _extract_bearer(raw: str | None) -> str | None:
    if not raw:
        return None
    parts = raw.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1]:
        return parts[1]
    return None


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
    header_token: str | None = Depends(oauth2_scheme),
):
    token = header_token or _extract_bearer(request.cookies.get("access_token"))

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str) or not email:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from None

    user = await user_repository.get_user_by_email(session=session, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

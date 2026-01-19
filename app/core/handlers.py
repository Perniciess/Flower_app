from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    InsufficientPermission,
    PasswordsDoNotMatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


async def user_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(UserNotFoundError, exc)

    content: dict[str, object] = {"detail": str(e)}
    if e.user_id is not None:
        content["user_id"] = e.user_id
    if e.email is not None:
        content["email"] = e.email

    return JSONResponse(status_code=404, content=content)


async def user_exists_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(UserAlreadyExistsError, exc)
    return JSONResponse(status_code=409, content={"detail": str(e), "email": e.email})


async def password_not_match_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(PasswordsDoNotMatchError, exc)
    return JSONResponse(status_code=400, content={"detail": str(e)})


async def insufficient_permission(request: Request, exc: Exception) -> JSONResponse:
    e = cast(InsufficientPermission, exc)
    return JSONResponse(status_code=400, content={"detail": str(e)})

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError


async def user_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, UserNotFoundError)

    content: dict[str, object] = {"detail": str(exc)}
    if exc.user_id is not None:
        content["user_id"] = exc.user_id
    if exc.email is not None:
        content["email"] = exc.email
    return JSONResponse(status_code=404, content=content)


async def user_exists_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, UserAlreadyExistsError)

    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "email": exc.email},
    )

from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import (
    CartAlreadyExistsError,
    CartItemNotFoundError,
    CartNotFoundError,
    FlowerNotFoundError,
    ImageNotFoundError,
    InsufficientPermissionError,
    InvalidTokenError,
    PasswordsDoNotMatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


async def user_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(UserNotFoundError, exc)

    content: dict[str, object] = {"detail": str(e)}
    if e.user_id is not None:
        content["user_id"] = e.user_id
    if e.phone_number is not None:
        content["phone_number"] = e.phone_number

    return JSONResponse(status_code=404, content=content)


async def user_exists_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(UserAlreadyExistsError, exc)
    return JSONResponse(status_code=409, content={"detail": str(e), "phone_number": e.phone_number})


async def password_not_match_handler(request: Request, exc: Exception) -> JSONResponse:
    e = cast(PasswordsDoNotMatchError, exc)
    return JSONResponse(status_code=400, content={"detail": str(e)})


async def insufficient_permission(request: Request, exc: Exception) -> JSONResponse:
    e = cast(InsufficientPermissionError, exc)
    return JSONResponse(status_code=403, content={"detail": str(e)})


async def invalid_token(request: Request, exc: Exception) -> JSONResponse:
    e = cast(InvalidTokenError, exc)
    return JSONResponse(status_code=403, content={"detail": str(e)})


async def flower_not_found(request: Request, exc: Exception) -> JSONResponse:
    e = cast(FlowerNotFoundError, exc)
    return JSONResponse(status_code=404, content={"detail": str(e)})


async def image_not_found(request: Request, exc: Exception) -> JSONResponse:
    e = cast(ImageNotFoundError, exc)
    return JSONResponse(status_code=404, content={"detail": str(e)})


async def cart_already_exists(request: Request, exc: Exception) -> JSONResponse:
    e = cast(CartAlreadyExistsError, exc)
    return JSONResponse(status_code=409, content={"detail": str(e)})


async def cart_not_found(request: Request, exc: Exception) -> JSONResponse:
    e = cast(CartNotFoundError, exc)
    return JSONResponse(status_code=404, content={"detail": str(e)})


async def cart_item_not_found(request: Request, exc: Exception) -> JSONResponse:
    e = cast(CartItemNotFoundError, exc)
    return JSONResponse(status_code=404, content={"detail": str(e)})

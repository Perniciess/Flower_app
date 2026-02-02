from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


def sqlalchemy_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    if isinstance(_exc, SQLAlchemyError):
        return JSONResponse(status_code=500, content={"detail": "Database error"})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

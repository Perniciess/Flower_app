import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = structlog.get_logger(__name__)


def sqlalchemy_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    if isinstance(_exc, SQLAlchemyError):
        logger.exception("sqlalchemy_error", exc_info=_exc, error_type=type(_exc).__name__)
        return JSONResponse(status_code=500, content={"detail": "Database error"})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid.uuid4())

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        start_time = time.time()
        logger.info(
            "request_started",
            query_params=dict(request.query_params) if request.query_params else None,
        )

        try:
            response = await call_next(request)

            duration = time.time() - start_time
            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            duration = time.time() - start_time
            logger.exception(
                "request_failed",
                exc_info=exc,
                duration_ms=round(duration * 1000, 2),
            )
            raise

        finally:
            structlog.contextvars.clear_contextvars()

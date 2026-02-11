import asyncio
import re
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from scalar_fastapi import get_scalar_api_reference
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware
from starlette_csrf.middleware import CSRFMiddleware

from app.api.v1.auth_router import auth_router
from app.api.v1.banners_router import banner_router
from app.api.v1.carts_router import cart_router
from app.api.v1.categories_router import category_router
from app.api.v1.discounts_router import discount_router
from app.api.v1.favourites_router import favourite_router
from app.api.v1.flowers_router import flower_router
from app.api.v1.orders_router import order_router
from app.api.v1.pickups_router import pickup_point_router
from app.api.v1.products_router import product_router
from app.api.v1.users_router import user_router
from app.core.config import settings
from app.core.handlers import sqlalchemy_exception_handler, unhandled_exception_handler
from app.core.limiter import init_limiter, limiter
from app.core.logger import get_logger, setup_logging
from app.core.logging_middleware import LoggingMiddleware
from app.core.redis import get_redis, redis_manager
from app.core.security_headers_middleware import SecurityHeadersMiddleware
from app.db.session import AsyncSessionLocal, engine
from app.repository import auth_repository

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup", environment=settings.ENVIRONMENT)

    logger.info("static_directories_created", upload_dir=str(settings.STATIC_FILES_DIR))

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("database_connected", db=settings.POSTGRES_DB)
    except Exception as exc:
        logger.exception("database_connection_failed", exc_info=exc)
        raise

    try:
        await redis_manager.init_pool()
        redis = get_redis()
        await redis.ping()  # type: ignore[misc]
        await redis.aclose()
        logger.info("redis_connected", url=settings.REDIS_URL.split("@")[-1])
    except Exception as exc:
        logger.exception("redis_connection_failed", exc_info=exc)
        raise
    try:
        init_limiter()
        app.state.limiter = limiter
        logger.info("limiter_started", url=settings.REDIS_URL.split("@")[-1])
    except Exception as exc:
        logger.exception("limiter_failed", exc_info=exc)
        raise

    async def _cleanup_expired_tokens():
        while True:
            try:
                await asyncio.sleep(3600)
                async with AsyncSessionLocal() as session:
                    deleted = await auth_repository.delete_expired_tokens(
                        session=session
                    )
                    await session.commit()
                    if deleted > 0:
                        logger.info("tokens_cleanup", deleted_count=deleted)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.exception("tokens_cleanup_failed", exc_info=exc)

    cleanup_task = asyncio.create_task(_cleanup_expired_tokens())

    yield

    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass

    logger.info("application_shutdown")
    await redis_manager.close_pool()
    await engine.dispose()


app = FastAPI(
    title="FlowerShop API",
    description="API для магазина цветов",
    openapi_tags=[
        {"name": "users", "description": "Операции с пользователями"},
        {"name": "auth", "description": "Аутентификация и авторизация"},
        {"name": "products", "description": "Операции с товарами"},
        {"name": "carts", "description": "Корзина покупок"},
        {"name": "pickup_points", "description": "Точки самовывоза"},
    ],
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )


app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # type: ignore
)

app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

csrf_header_scheme = APIKeyHeader(name=settings.CSRF_HEADER_NAME, auto_error=False)

app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CSRFMiddleware,
    cookie_httponly=True,
    secret=settings.CSRF_SECRET_KEY,
    cookie_name=settings.CSRF_COOKIE_NAME,
    header_name=settings.CSRF_HEADER_NAME,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_samesite=settings.COOKIE_SAMESITE,
    sensitive_cookies={"__Host-rt", "rt"},
    exempt_urls=[
        re.compile(r"/docs"),
        re.compile(r"/openapi.json"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/login"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/refresh"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/complete-register/[^/]+$"),
        re.compile(
            re.escape(settings.API_V1_STR) + r"/auth/complete-reset-verification/[^/]+$"
        ),
        re.compile(re.escape(settings.API_V1_STR) + r"/orders/webhook"),
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", settings.CSRF_HEADER_NAME],
)

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(cart_router)
api_router.include_router(order_router)
api_router.include_router(category_router)
api_router.include_router(favourite_router)
api_router.include_router(discount_router)
api_router.include_router(pickup_point_router)
api_router.include_router(flower_router)
api_router.include_router(banner_router)
app.include_router(api_router, dependencies=[Depends(csrf_header_scheme)])


settings.ROOT_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    f"/{settings.STATIC_FILES_DIR}",
    StaticFiles(directory=settings.ROOT_DIR),
    name="static",
)

add_pagination(app)

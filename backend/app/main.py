import re
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import APIKeyHeader
from fastapi_pagination import add_pagination
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from starlette_csrf.middleware import CSRFMiddleware

from app.core.config import settings
from app.core.limiter import limiter
from app.core.redis import get_redis, redis_manager
from app.database.session import engine
from app.modules.auth.router import auth_router
from app.modules.carts.router import cart_router
from app.modules.categories.router import category_router
from app.modules.discounts.router import discount_router
from app.modules.favourites.router import favourite_router
from app.modules.orders.router import order_router
from app.modules.pickup_points.router import pickup_point_router
from app.modules.products.router import product_router
from app.modules.users.router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("DB connected")
    except Exception as exc:
        print(f"DB connection failed: {exc}")
        raise
    try:
        await redis_manager.init_pool()
        redis = get_redis()
        await redis.ping()  # type: ignore[misc]
        await redis.aclose()
        print("Redis connected")
    except Exception as exc:
        print(f"Redis connection failed: {exc}")
        raise
    yield
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

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # type: ignore
)

csrf_header_scheme = APIKeyHeader(name=settings.CSRF_HEADER_NAME, auto_error=False)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(
    CSRFMiddleware,
    cookie_httponly=True,
    secret=settings.CSRF_SECRET_KEY,
    cookie_name=settings.CSRF_COOKIE_NAME,
    header_name=settings.CSRF_HEADER_NAME,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_samesite="strict",
    sensitive_cookies={"access_token"},
    exempt_urls=[
        re.compile(r"/docs"),
        re.compile(r"/openapi.json"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/login"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/complete-register/.*"),
        re.compile(re.escape(settings.API_V1_STR) + r"/auth/complete-reset-verification/.*"),
        re.compile(re.escape(settings.API_V1_STR) + r"/orders/webhook"),
    ],
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
app.include_router(api_router, dependencies=[Depends(csrf_header_scheme)])


add_pagination(app)

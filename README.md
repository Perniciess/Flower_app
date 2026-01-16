# Flower Shop API

FastAPI backend для мобильного приложения магазина цветов.

## Описание

REST API для управления каталогом цветов, корзиной покупок и заказами. Поддерживает регистрацию пользователей, аутентификацию и управление товарами.

## Стек

- **FastAPI** — современный веб-фреймворк для создания API
- **SQLAlchemy 2.0** — ORM для работы с базой данных
- **PostgreSQL** — реляционная база данных
- **Alembic** — миграции базы данных
- **Pydantic** — валидация данных
- **pwdlib** — хэширование паролей
- **asyncpg** — асинхронный драйвер PostgreSQL

## Структура проекта
```
FlowerShop_FastAPI/
├─ app/
│  ├─ core/
│  │  ├─ config.py          # Settings / env config
│  │  ├─ security.py        # JWT, password hashing
│  │  ├─ exceptions.py      # Custom exceptions
│  │  └─ handlers.py        # Exception handlers
│  ├─ database/
│  │  ├─ base.py            # DeclarativeBase
│  │  └─ session.py         # AsyncSession, engine, get_db
│  ├─ models/
│  │  └─ user.py            # SQLAlchemy model User
│  ├─ schemas/
│  │  └─ user_schemas.py    # Pydantic schemas
│  ├─ repositories/
│  │  └─ user_repository.py # DB layer
│  ├─ services/
│  │  └─ user_service.py    # Business logic
│  ├─ routers/
│  │  └─ user_router.py     # API endpoints
│  └─ main.py               # FastAPI app entrypoint
├─ alembic/
├─ alembic.ini
├─ pyproject.toml
└─ README.md
```

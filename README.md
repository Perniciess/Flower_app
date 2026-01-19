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
│ ├─ core/
│ │ ├─ init.py
│ │ ├─ config.py # Settings / env config
│ │ ├─ deps.py # Dependencies
│ │ ├─ security.py # JWT, password hashing
│ │ ├─ exceptions.py # Custom exceptions
│ │ └─ handlers.py # Exception handlers
│ ├─ database/
│ │ ├─ init.py
│ │ ├─ base.py # DeclarativeBase
│ │ └─ session.py # AsyncSession, engine, get_db
│ ├─ modules/
│ │ ├─ auth/
│ │ │ ├─ init.py
│ │ │ ├─ model.py # Auth model
│ │ │ ├─ schema.py # Pydantic schemas
│ │ │ ├─ repository.py # DB layer
│ │ │ ├─ service.py # Business logic
│ │ │ ├─ router.py # API endpoints
│ │ │ └─ utils.py # Helper functions
│ │ └─ users/
│ │ ├─ init.py
│ │ ├─ model.py # User model
│ │ ├─ schema.py # Pydantic schemas
│ │ ├─ repository.py # DB layer
│ │ ├─ service.py # Business logic
│ │ └─ router.py # API endpoints
│ ├─ init.py
│ └─ main.py # FastAPI app entrypoint
├─ alembic/
├─ docker/
├─ DEVELOPMENT.md
└─ README.md
```

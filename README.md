# Flower Shop

REST API и Telegram бот для магазина цветов.

## Описание

Проект состоит из двух частей:
- **Backend** — REST API для управления каталогом цветов, корзиной и пользователями
- **Bot** — Telegram бот для верификации номера телефона при регистрации

## Стек

### Backend
- **FastAPI** — веб-фреймворк для API
- **SQLAlchemy 2.0** — async ORM
- **PostgreSQL** — база данных
- **Redis** — JWT blacklist, verification tokens
- **Alembic** — миграции
- **Pydantic** — валидация данных
- **pwdlib** — хеширование паролей (Argon2)

### Bot
- **aiogram 3** — Telegram Bot API
- **Redis** — FSM storage

## Структура проекта

```
Flower_shop/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Settings
│   │   │   ├── deps.py            # Dependencies (get_current_user)
│   │   │   ├── exceptions.py      # Custom exceptions
│   │   │   ├── handlers.py        # Exception handlers
│   │   │   ├── redis.py           # Redis manager
│   │   │   └── security.py        # JWT, password hashing, blacklist
│   │   ├── database/
│   │   │   ├── base.py            # DeclarativeBase
│   │   │   └── session.py         # AsyncSession, engine
│   │   ├── modules/
│   │   │   ├── auth/              # Auth module
│   │   │   │   ├── model.py      
│   │   │   │   ├── schema.py      
│   │   │   │   ├── repository.py  
│   │   │   │   ├── service.py     
│   │   │   │   ├── router.py    
│   │   │   │   └── utils.py      
│   │   │   ├── users/             # Users module
│   │   │   │   ├── model.py      
│   │   │   │   ├── schema.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   ├── flowers/           # Flowers module
│   │   │   │   ├── model.py       
│   │   │   │   ├── schema.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   └── carts/             # Carts module
│   │   │       ├── model.py       
│   │   │       ├── schema.py
│   │   │       ├── repository.py
│   │   │       ├── service.py
│   │   │       └── router.py
│   │   └── main.py                # FastAPI entrypoint
│   └── alembic/                   # Migrations
│
├── bot/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Settings
│   │   │   └── redis.py           # RedisManager
│   │   ├── handlers/
│   │   │   └── handler.py         # Message handlers
│   │   ├── keyboards/
│   │   │   └── phone.py           # Contact keyboard
│   │   ├── service/
│   │   │   └── registration.py    # Backend API calls
│   │   ├── states/
│   │   │   └── registration.py    # FSM states
│   │   └── __main__.py            # Bot entrypoint
│
└── docker/                        # Docker configs
```

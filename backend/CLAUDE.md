# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flower Shop is a monorepo with two Python 3.13+ applications:
- **backend/** — FastAPI REST API for product catalog, shopping carts, orders, and users
- **bot/** — Telegram bot (aiogram 3) for phone number verification during registration

## Commands

### Backend (from `backend/` directory)
```bash
uv sync                                    # Install dependencies
fastapi dev app/main.py                    # Run development server (port 8000)
alembic revision --autogenerate -m "msg"   # Create migration
alembic upgrade head                       # Apply migrations
ruff check app/                            # Lint
ruff format app/                           # Format
```

### Bot (from `bot/` directory)
```bash
uv sync                                    # Install dependencies
python -m app                              # Run bot
ruff check app/ && ruff format app/        # Lint and format
```

### Infrastructure
```bash
docker compose --env-file .env -f docker/docker-compose.yaml up -d  # Start PostgreSQL + Redis
```

## Architecture

### Layer-Based Structure
The backend uses a horizontal (layered) architecture. Each layer is a top-level directory under `backend/app/`, and features are separated by file name:

```
backend/app/
├── api/v1/          — FastAPI routers ({feature}_router.py)
├── models/          — SQLAlchemy ORM models ({feature}_model.py)
├── schemas/         — Pydantic request/response schemas ({feature}_schema.py)
├── repository/      — Database queries, async ({feature}_repository.py)
├── service/         — Business logic ({feature}_service.py)
├── core/            — Config, security, deps, exceptions, rate limiter, Redis
├── db/              — Database base model and async session factory
├── utils/           — Validators (image, password, phone) and filters (products)
└── static/uploads/  — Uploaded images (products, categories)
```

Features: `auth`, `users`, `products`, `categories`, `carts`, `orders`, `discounts`, `favourites`, `pickups`, `payments`

### Authentication Flow
1. Frontend sends registration data → Backend stores in Redis with verification token (5-min TTL)
2. User opens Telegram deeplink → Bot validates token and requests phone contact
3. Bot verifies phone matches → Calls `/auth/complete-register/{token}`
4. Backend creates user in PostgreSQL, issues JWT access (15min) + refresh (30d) tokens as HTTP-only cookies

### Key Dependencies
- `backend/app/core/deps.py` — `get_current_user`, role-based access (`require_admin`, `require_client`), Yookassa webhook verification
- `backend/app/core/security.py` — JWT handling, password hashing (Argon2), token blacklist
- `backend/app/core/redis.py` — Redis connection management
- `backend/app/core/limiter.py` — Rate limiting (slowapi)
- `backend/app/core/exceptions.py` — Custom exception classes
- `backend/app/db/session.py` — AsyncSession factory

### Roles
- `Role.CLIENT` — Default user role
- `Role.ADMIN` — Administrator access

## Code Style

- Ruff enforces: E, F, I, UP, B, PERF, FIX002, PLE, PLW, F822, N, S, RUF, ASYNC rules
- Line length: 120 characters
- Google-style docstrings, double quotes
- Russian allowed in strings (Cyrillic confusables permitted)
- All database operations are async

## Environment Variables

Backend requires: `SECRET_KEY`, `CSRF_SECRET_KEY`, `POSTGRES_*`, `REDIS_URL`, `FRONTEND_HOST`, `YOOKASSA_SHOP_ID`, `YOOKASSA_SECRET_KEY`, `PROJECT_NAME`
Bot requires: `BOT_TOKEN`, `REDIS_URL`, `BACKEND_URL`, `WEBSITE_URL`

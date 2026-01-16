docker compose --env-file .env -f docker/docker-compose.yaml up -d


app/
  main.py              # точка входа (FastAPI())
  api/
    v1/
      routers/         # файлы с роутерами
        users.py
        auth.py
      deps.py          # зависимости (get_db, get_current_user)
  core/
    config.py          # настройки (env, окружение)
    security.py        # JWT, hashing, auth-утилиты
    exceptions.py      # общие исключения/обработчики
  models/              # ORM-модели (SQLAlchemy)
    user.py
  schemas/             # Pydantic-схемы (in/out)
    user.py
    auth.py
  services/            # бизнес-логика (use-cases)
    user_service.py
    auth_service.py
  repositories/        # доступ к БД
    user_repository.py
  db/
    base.py            # Base = declarative base
    session.py         # создание SessionLocal / async session
    migrations/        # миграции (alembic)
  utils/               # вспомогательные функции
tests/
  conftest.py
  test_users.py

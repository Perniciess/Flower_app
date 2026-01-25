docker compose --env-file .env -f docker/docker-compose.yaml up -d

fastapi dev app/main.py

alembic revision --autogenerate -m "your message"
alembic upgrade head

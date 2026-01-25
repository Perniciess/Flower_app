from redis.asyncio import ConnectionPool, Redis

from .config import settings


class RedisManager:
    """Класс для работы с Redis."""

    def __init__(self):
        self.pool: ConnectionPool | None = None

    async def init_pool(self) -> None:
        """Инициализация пула."""
        self.pool = ConnectionPool.from_url(f"{settings.REDIS_URL}", max_connections=10, decode_responses=True)

    async def close_pool(self) -> None:
        """Закрытие пула."""
        if self.pool:
            await self.pool.disconnect()
            self.pool = None

    def get_client(self) -> Redis:
        """Создаение клиента из существующего пула."""
        if self.pool is None:
            raise RuntimeError("Redis pool is not initialized. Call init_pool() first.")
        return Redis(connection_pool=self.pool)


redis_manager = RedisManager()


def get_redis() -> Redis:
    return redis_manager.get_client()

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import ConnectionPool, Redis

from .config import settings


class RedisManager:
    """Класс для работы с Redis."""

    def __init__(self):
        self.pool: ConnectionPool | None = None
        self.storage: RedisStorage | None = None

    async def init_pool(self) -> None:
        """Инициализация пула."""
        self.pool = ConnectionPool.from_url(settings.REDIS_URL, max_connections=10, decode_responses=True)
        redis = Redis(connection_pool=self.pool)
        self.storage = RedisStorage(redis=redis, state_ttl=300, data_ttl=300)

    async def close_pool(self) -> None:
        """Закрытие пула."""
        if self.pool:
            await self.pool.disconnect()
            self.pool = None

    def get_client(self) -> Redis:
        """Создаение клиента из существующего пула."""
        if self.pool is None:
            raise RuntimeError("Redis pool not initialized")
        return Redis(connection_pool=self.pool)

    def get_storage(self) -> RedisStorage:
        """Получение RedisStorage для FSM."""
        if self.storage is None:
            raise RuntimeError("Redis storage not initialized")
        return self.storage


redis_manager = RedisManager()

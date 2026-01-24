from redis.asyncio import ConnectionPool, Redis

from .config import settings

pool: ConnectionPool | None = None


async def init_redis_pool() -> None:
    global pool
    pool = ConnectionPool.from_url(f"{settings.REDIS_URL}", max_connections=10, decode_responses=True)


async def close_redis_pool() -> None:
    if pool:
        await pool.disconnect()


def get_redis() -> Redis:
    if pool is None:
        raise RuntimeError("Redis pool is not initialized")
    return Redis(connection_pool=pool)

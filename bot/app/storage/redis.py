from aiogram.fsm.storage.redis import RedisStorage

from app.core.config import settings

storage = RedisStorage.from_url(settings.REDIS_URL, state_ttl=300, data_ttl=300)

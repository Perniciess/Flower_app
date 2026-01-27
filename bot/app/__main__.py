import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings
from app.core.redis import redis_manager
from app.handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await redis_manager.init_pool()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=redis_manager.get_storage())
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await redis_manager.close_pool()


if __name__ == "__main__":
    asyncio.run(main())

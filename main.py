import asyncio
from aiogram import Bot, Dispatcher

from config import settings
from services.memory import init_memory_db
from services.queue import queue_worker

from handlers.brand import router as brand_router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(brand_router)


async def main():
    await init_memory_db()

    asyncio.create_task(queue_worker())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

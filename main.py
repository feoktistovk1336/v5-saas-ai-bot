from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.content import router as content_router
from handlers.rewrite import router as rewrite_router
from handlers.admin import router as admin_router
from handlers.payments import router as payments_router

from database.db import init_db


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


async def startup():

    await init_db()

    dp.include_router(start_router)
    dp.include_router(content_router)
    dp.include_router(rewrite_router)
    dp.include_router(admin_router)
    dp.include_router(payments_router)

    print("🚀 PRIMEONIX AI STARTED")


async def main():

    await startup()

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())

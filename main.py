import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CHANNEL_ID
)

from ai import generate_text
from media import (
    generate_images,
    generate_reels_text
)

from db import (
    init_db,
    create_user
)

from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)


# ================= BOT =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

scheduler = AsyncIOScheduler()


# ================= MENU =================
menu = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="🔥 AI Пост"),
            KeyboardButton(text="🖼 Карусель")
        ],

        [
            KeyboardButton(text="🎬 Reels"),
            KeyboardButton(text="🧠 Идеи")
        ],

        [
            KeyboardButton(text="📈 Тренды"),
            KeyboardButton(text="💳 Тарифы")
        ],

        [
            KeyboardButton(text="👑 Админ")
        ]

    ],
    resize_keyboard=True
)


# ================= START =================
@dp.message(lambda m: m.text == "/start")
async def start(m: types.Message):

    await create_user(m.from_user.id)

    await m.answer(
        "🚀 Добро пожаловать в V5 AI SaaS\n\n"
        "Создавай AI контент за секунды.",
        reply_markup=menu
    )


# ================= AI POST =================
@dp.message(lambda m: m.text == "🔥 AI Пост")
async def ai_post(m: types.Message):

    try:

        await m.answer(
            "🔥 Создаю AI пост..."
        )

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            1
        )

        if images:

            await m.answer_photo(
                photo=images[0],
                caption=text[:1000]
            )

        else:

            await m.answer(text[:4000])

    except Exception as e:

        print("AI ERROR:", e)

        await m.answer(
            "❌ Ошибка генерации поста"
        )


# ================= CAROUSEL =================
@dp.message(lambda m: m.text == "🖼 Карусель")
async def carousel(m: types.Message):

    try:

        await m.answer(
            "🖼 Создаю AI карусель..."
        )

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            5
        )

        print(images)

        if not images:

            return await m.answer(
                "❌ Картинки не создались"
            )

        # отправляем картинки
        for img in images:

            try:

                await m.answer_photo(
                    photo=img
                )

            except Exception as img_error:

                print(
                    "IMAGE ERROR:",
                    img_error
                )

        # отправляем текст
        await m.answer(
            f"🖼 AI Карусель\n\n{text[:4000]}"
        )

    except Exception as e:

        print("CAROUSEL ERROR:", e)

        await m.answer(
            "❌ Ошибка карусели"
        )


# ================= REELS =================
@dp.message(lambda m: m.text == "🎬 Reels")
async def reels(m: types.Message):

    try:

        await m.answer(
            "🎬 Создаю Reels..."
        )

        text, topic = await generate_text()

        script = await generate_reels_text(
            topic
        )

        await m.answer(
            f"{script}\n\n{text[:2000]}"
        )

    except Exception as e:

        print("REELS ERROR:", e)

        await m.answer(
            "❌ Ошибка генерации Reels"
        )


# ================= IDEAS =================
@dp.message(lambda m: m.text == "🧠 Идеи")
async def ideas(m: types.Message):

    ideas_list = [

        "5 AI-инструментов для бизнеса",
        "Как заработать на нейросетях",
        "AI vs дизайнеры",
        "Лучшие GPT для работы",
        "Как автоматизировать контент",
        "Как AI меняет маркетинг",
        "Нейросети для TikTok",
        "AI для Instagram",
        "Будущее AI бизнеса",
        "Как создать AI SaaS"

    ]

    random.shuffle(ideas_list)

    text = "\n".join(
        ideas_list[:5]
    )

    await m.answer(
        f"🧠 AI ИДЕИ\n\n{text}"
    )


# ================= TRENDS =================
@dp.message(lambda m: m.text == "📈 Тренды")
async def trends(m: types.Message):

    await m.answer(
        "📈 AI ТРЕНДЫ 2026\n\n"

        "🔥 AI агенты\n"
        "🔥 TikTok automation\n"
        "🔥 Faceless YouTube\n"
        "🔥 AI инфобизнес\n"
        "🔥 AI видео\n"
        "🔥 AI SaaS\n"
        "🔥 AI маркетинг\n"
        "🔥 AI контент"
    )


# ================= TARIFFS =================
@dp.message(lambda m: m.text == "💳 Тарифы")
async def tariffs(m: types.Message):

    await m.answer(
        "💎 ТАРИФЫ V5 AI\n\n"

        "🆓 FREE\n"
        "• 5 AI постов\n"
        "• 1 карусель\n"
        "• 1 reels\n\n"

        "🚀 PRO — 990₽/мес\n"
        "• Безлимит AI постов\n"
        "• Безлимит каруселей\n"
        "• AI Reels\n"
        "• Premium AI\n\n"

        "💳 Оплата скоро появится"
    )


# ================= ADMIN =================
@dp.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):

    if m.from_user.id != ADMIN_ID:

        return await m.answer(
            "❌ Нет доступа"
        )

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        "/users\n"
        "/stats"
    )


# ================= AUTO POST =================
async def auto_post():

    try:

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            1
        )

        if images:

            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=images[0],
                caption=text[:1000]
            )

        else:

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=text[:4000]
            )

        print("AUTO POST SUCCESS")

    except Exception as e:

        print("AUTO POST ERROR:", e)


# ================= STARTUP =================
async def on_startup():

    await init_db()

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    scheduler.add_job(
        auto_post,
        "interval",
        hours=3
    )

    scheduler.start()

    print("БОТ ЗАПУЩЕН")


# ================= MAIN =================
async def main():

    await on_startup()

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

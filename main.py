import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from config import BOT_TOKEN, ADMIN_ID

from ai import generate_text

from media import (
    generate_images,
    generate_reels_text
)

from db import (
    init_db,
    create_user
)


# ================= BOT =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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
        "Создавай AI-контент за секунды.",
        reply_markup=menu
    )


# ================= AI POST =================
@dp.message(lambda m: m.text == "🔥 AI Пост")
async def ai_post(m: types.Message):

    try:

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            1
        )

        # если картинка есть
        if images:

            await m.answer_photo(
                photo=images[0],
                caption=text
            )

        else:

            await m.answer(text)

    except Exception as e:

        print("AI ERROR:", e)

        await m.answer(
            "❌ Ошибка генерации поста"
        )


# ================= CAROUSEL =================
@dp.message(lambda m: m.text == "🖼 Карусель")
async def carousel(m: types.Message):

    try:

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            5
        )

        if not images:

            return await m.answer(
                "❌ Картинки не сгенерированы"
            )

        # отправляем по одной картинке
        for img in images:

            await m.answer_photo(
                photo=img
            )

        # потом текст
        await m.answer(text)

    except Exception as e:

        print("CAROUSEL ERROR:", e)

        await m.answer(
            "❌ Ошибка карусели"
        )


# ================= REELS =================
@dp.message(lambda m: m.text == "🎬 Reels")
async def reels(m: types.Message):

    try:

        text, topic = await generate_text()

        script = f"""
🎬 AI REELS

🔥 Хук:
Ты не готов к тому, как AI меняет рынок прямо сейчас...

📌 Тема:
{topic}

🧠 Сценарий:
{text}

🚀 Призыв:
Подпишись, чтобы получать больше AI-контента.
"""

        await m.answer(script)

    except Exception as e:

        print("REELS ERROR:", e)

        await m.answer(
            "❌ Ошибка генерации Reels"
        )


# ================= IDEAS =================
@dp.message(lambda m: m.text == "🧠 Идеи")
async def ideas(m: types.Message):

    await m.answer(
        "💡 ИДЕИ ДЛЯ КОНТЕНТА\n\n"

        "1. 5 AI-инструментов для бизнеса\n"
        "2. Как заработать на нейросетях\n"
        "3. AI vs дизайнеры\n"
        "4. Лучшие GPT для работы\n"
        "5. Как автоматизировать контент"
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
        "🔥 AI видео"
    )


# ================= UPGRADE =================
@dp.message(lambda m: m.text == "💳 Тарифы")
async def upgrade(m: types.Message):

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
        "• Приоритет генерации\n"
        "• Premium AI\n\n"

        "💳 Оплата появится скоро"
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
        "/users - список пользователей\n"
        "/stats - статистика системы"
    )


# ================= MAIN =================
async def main():

    await init_db()

    # удаляем webhook
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    # запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

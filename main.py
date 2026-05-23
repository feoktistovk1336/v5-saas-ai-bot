import asyncio
import os
import random
import aiohttp

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from aiogram import Bot, Dispatcher, types

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CHANNEL_ID
)

from ai import generate_text

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
# ================= SCHEDULER =================
scheduler = AsyncIOScheduler()

# ================= IMAGE GENERATOR =================
async def generate_images(prompt: str, count=5):

    images = []

    os.makedirs("temp", exist_ok=True)

    async with aiohttp.ClientSession() as session:

        for i in range(count):

            seed = random.randint(1, 999999)

            filename = f"temp/{seed}.jpg"

            # ================= AI IMAGE =================
            url = (
                f"https://image.pollinations.ai/prompt/"
                f"beautiful%20{prompt}%20ai%20art"
                f"?width=1024&height=1024"
                f"&seed={seed}"
                f"&model=flux"
            )

            try:

                async with session.get(url) as r:

                    # ================= FALLBACK =================
                    if r.status != 200:

                        print("POLLINATIONS FAILED:", r.status)

                        fallback = (
                            f"https://picsum.photos/seed/"
                            f"{seed}/1024/1024"
                        )

                        async with session.get(fallback) as f:

                            if f.status == 200:

                                with open(filename, "wb") as img_file:
                                    img_file.write(await f.read())

                    else:

                        with open(filename, "wb") as img_file:
                            img_file.write(await r.read())

                # ================= DESIGN =================
                img = Image.open(filename)

                img = img.resize((1080, 1080))

                overlay = Image.new(
                    "RGBA",
                    img.size,
                    (0, 0, 0, 120)
                )

                img = Image.alpha_composite(
                    img.convert("RGBA"),
                    overlay
                )

                draw = ImageDraw.Draw(img)

                # ================= FONT =================
                try:

                    font = ImageFont.truetype(
                        "arial.ttf",
                        60
                    )

                except:

                    font = ImageFont.load_default()

                # ================= TITLE =================
                title = prompt.upper()[:35]

                draw.text(
                    (60, 120),
                    title,
                    fill="white",
                    font=font
                )

                # ================= BRAND =================
                draw.text(
                    (60, 950),
                    "V5 AI SAAS",
                    fill="white",
                    font=font
                )

                img = img.convert("RGB")

                img.save(filename)

                images.append(
                    FSInputFile(filename)
                )

            except Exception as e:

                print("IMAGE ERROR:", e)

    return images


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

        if images:

            await m.answer_photo(
                photo=images[0],
                caption=text
            )

        else:

            await m.answer(text)

    except Exception as e:

        print("AI POST ERROR:", e)

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

        for img in images:

            await m.answer_photo(
                photo=img
            )

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
Подпишись на V5 AI SaaS
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
                caption=text
            )

        else:

            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=text
            )

        print("AUTO POST SENT")

    except Exception as e:

        print("AUTOPOST ERROR:", e)


# ================= AUTO CAROUSEL =================
async def auto_carousel():

    try:

        text, topic = await generate_text()

        images = await generate_images(
            topic,
            5
        )

        for img in images:

            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=img
            )

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )

        print("AUTO CAROUSEL SENT")

    except Exception as e:

        print("AUTO CAROUSEL ERROR:", e)
        
# ================= MAIN =================
async def main():

    await init_db()

    # удаляем старый webhook
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    print("BOT STARTED")

    # ================= SCHEDULE =================
    scheduler.add_job(
        auto_post,
        "interval",
        hours=6
    )

    scheduler.add_job(
        auto_carousel,
        "interval",
        hours=12
    )

    scheduler.start()

    # запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

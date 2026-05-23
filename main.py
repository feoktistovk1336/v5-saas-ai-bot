import asyncio
import random
import aiohttp

from PIL import Image, ImageDraw, ImageFont

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile

from config import BOT_TOKEN, ADMIN_ID, CHANNEL_ID
from ai import generate_text, generate_carousel
from media import generate_images, generate_reels_text
from db import init_db, create_user

from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 AI Пост"), KeyboardButton(text="🖼 Карусель")],
        [KeyboardButton(text="🎬 Reels"), KeyboardButton(text="🧠 Идеи")],
        [KeyboardButton(text="📈 Тренды"), KeyboardButton(text="💳 Тарифы")],
        [KeyboardButton(text="👑 Админ"), KeyboardButton(text="🚀 Автопост")]
    ],
    resize_keyboard=True
)


def wrap_text(text, max_chars=16):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        if len(line + " " + word) <= max_chars:
            line += " " + word
        else:
            lines.append(line.strip())
            line = word

    if line:
        lines.append(line.strip())

    return lines[:3]


async def create_ai_image(image_url, title):
    try:
        temp_file = f"temp_{random.randint(1, 999999)}.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    return None

                content = await response.read()

                with open(temp_file, "wb") as f:
                    f.write(content)

        image = Image.open(temp_file).convert("RGBA")
        image = image.resize((1080, 1080))

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 70))
        image = Image.alpha_composite(image, overlay)

        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                72
            )
            small_font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                34
            )
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        draw.rounded_rectangle(
            [(45, 600), (1035, 1015)],
            radius=42,
            fill=(0, 0, 0, 190)
        )

        lines = wrap_text(f"🔥 {title.upper()}", 16)

        y = 660
        for line in lines:
            draw.text((80, y), line, fill=(255, 255, 255), font=font)
            y += 90

        draw.text(
            (80, 925),
            "V5 AI SAAS",
            fill=(120, 255, 160),
            font=small_font
        )

        draw.text(
            (680, 925),
            "@v5_saas_ai_bot",
            fill=(220, 220, 220),
            font=small_font
        )

        final_file = f"final_{random.randint(1, 999999)}.jpg"

        image.convert("RGB").save(final_file, quality=95)

        return final_file

    except Exception as e:
        print("CREATE IMAGE ERROR:", e)
        return None


@dp.message(lambda m: m.text == "/start")
async def start(m: types.Message):
    await create_user(m.from_user.id)

    await m.answer(
        "🚀 Добро пожаловать в V5 AI SaaS\n\n"
        "Создавай AI контент за секунды.",
        reply_markup=menu
    )


@dp.message(lambda m: m.text == "🔥 AI Пост")
async def ai_post(m: types.Message):
    try:
        await m.answer("🔥 Создаю AI пост...")

        text, topic = await generate_text()
        images = await generate_images(topic, 1)

        if images:
            final_image = await create_ai_image(images[0], topic)

            if final_image:
                await m.answer_photo(photo=FSInputFile(final_image))

        await m.answer(text[:4000])

    except Exception as e:
        print("AI POST ERROR:", e)
        await m.answer("❌ Ошибка генерации поста")


@dp.message(lambda m: m.text == "🖼 Карусель")
async def carousel(m: types.Message):
    try:
        await m.answer("🖼 Создаю AI карусель...")

        topic = random.choice([
            "AI бизнес",
            "нейросети",
            "AI маркетинг",
            "AI стартапы",
            "AI контент"
        ])

        slides = await generate_carousel(topic)
        images = await generate_images(topic, len(slides))

        for i, slide in enumerate(slides):
            final_image = await create_ai_image(images[i], slide)

            if final_image:
                await m.answer_photo(photo=FSInputFile(final_image))

        await m.answer("🔥 AI карусель готова")

    except Exception as e:
        print("CAROUSEL ERROR:", e)
        await m.answer("❌ Ошибка карусели")


@dp.message(lambda m: m.text == "🎬 Reels")
async def reels(m: types.Message):
    try:
        await m.answer("🎬 Создаю Reels...")

        text, topic = await generate_text()
        script = await generate_reels_text(topic)

        await m.answer(f"{script}\n\n{text[:2000]}")

    except Exception as e:
        print("REELS ERROR:", e)
        await m.answer("❌ Ошибка генерации Reels")


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

    await m.answer(
        "🧠 AI ИДЕИ\n\n" +
        "\n".join(ideas_list[:5])
    )


@dp.message(lambda m: m.text == "📈 Тренды")
async def trends(m: types.Message):
    await m.answer(
        "📈 AI ТРЕНДЫ\n\n"
        "🔥 AI агенты\n"
        "🔥 TikTok automation\n"
        "🔥 Faceless YouTube\n"
        "🔥 AI инфобизнес\n"
        "🔥 AI видео\n"
        "🔥 AI SaaS\n"
        "🔥 AI маркетинг\n"
        "🔥 AI контент"
    )


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


@dp.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        "/postnow — пост сейчас\n"
        "/autostatus — статус автопоста"
    )


@dp.message(lambda m: m.text == "🚀 Автопост")
async def autopost_menu(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    await m.answer(
        "🚀 АВТОПОСТИНГ\n\n"
        "⏰ Сейчас: каждые 3 часа\n\n"
        "/postnow — выложить сейчас\n"
        "/autostatus — статус"
    )


async def auto_post():
    try:
        text, topic = await generate_text()
        images = await generate_images(topic, 1)

        if images:
            final_image = await create_ai_image(images[0], topic)

            if final_image:
                await bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=FSInputFile(final_image)
                )

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text[:4000]
        )

        print("AUTO POST SUCCESS")

    except Exception as e:
        print("AUTO POST ERROR:", e)


@dp.message(lambda m: m.text == "/postnow")
async def post_now(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return

    await m.answer("🚀 Публикую пост...")
    await auto_post()
    await m.answer("✅ Пост опубликован")


@dp.message(lambda m: m.text == "/autostatus")
async def auto_status(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return

    await m.answer(
        "✅ Автопостинг активен\n"
        "⏰ Интервал: 3 часа"
    )


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


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

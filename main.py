import asyncio
import os
import random
import aiohttp

from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, ADMIN_ID, CHANNEL_ID
from ai import generate_text, generate_carousel
from media import generate_images, generate_reels_text
from db import init_db, create_user, add_generation, get_stats


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

AUTOPOST_ENABLED = True


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
    lines, line = [], ""

    for word in words:
        test = f"{line} {word}".strip()
        if len(test) <= max_chars:
            line = test
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines[:4]


def load_font(size):
    paths = [
        "Montserrat-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass

    return ImageFont.load_default()


async def create_ai_image(image_url, title):
    try:
        temp_file = f"temp_{random.randint(1, 999999)}.jpg"
        final_file = f"final_{random.randint(1, 999999)}.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    return None

                with open(temp_file, "wb") as f:
                    f.write(await response.read())

        image = Image.open(temp_file).convert("RGBA")
        image = image.resize((1080, 1080))

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 80))
        image = Image.alpha_composite(image, overlay)

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(50, 560), (1030, 1015)],
            radius=45,
            fill=(0, 0, 0, 205)
        )

        font = load_font(78)
        small_font = load_font(34)

        lines = wrap_text(f"🔥 {title.upper()}", 15)

        y = 630
        for line in lines:
            draw.text(
                (85, y),
                line,
                fill=(255, 255, 255),
                font=font
            )
            y += 88

        draw.text(
            (85, 920),
            "V5 AI SAAS",
            fill=(120, 255, 160),
            font=small_font
        )

        draw.text(
            (650, 920),
            "@v5_saas_ai_bot",
            fill=(230, 230, 230),
            font=small_font
        )

        image.convert("RGB").save(final_file, quality=95)

        try:
            os.remove(temp_file)
        except:
            pass

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
        await add_generation(m.from_user.id, "post", text)

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

        await add_generation(m.from_user.id, "carousel", topic)

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

        await add_generation(m.from_user.id, "reels", script)

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
        "AI для TikTok",
        "AI для Instagram",
        "Как создать AI SaaS"
    ]

    random.shuffle(ideas_list)

    await m.answer("🧠 AI ИДЕИ\n\n" + "\n".join(ideas_list[:5]))


@dp.message(lambda m: m.text == "📈 Тренды")
async def trends(m: types.Message):
    await m.answer(
        "📈 AI ТРЕНДЫ\n\n"
        "🔥 AI агенты\n"
        "🔥 TikTok automation\n"
        "🔥 Faceless YouTube\n"
        "🔥 AI SaaS\n"
        "🔥 AI видео\n"
        "🔥 AI маркетинг"
    )


@dp.message(lambda m: m.text == "💳 Тарифы")
async def tariffs(m: types.Message):
    await m.answer(
        "💎 ТАРИФЫ V5 AI\n\n"
        "🆓 FREE\n"
        "• AI посты\n"
        "• Карусели\n"
        "• Reels scripts\n\n"
        "🚀 PRO — 990₽/мес\n"
        "• Безлимит\n"
        "• Автопостинг\n"
        "• Premium AI\n\n"
        "💳 Оплата скоро появится"
    )


@dp.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    users, gens = await get_stats()

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n\n"
        "/postnow — выложить сейчас\n"
        "/testpost — тест поста\n"
        "/autostatus — статус\n"
        "/autoon — включить\n"
        "/autooff — выключить"
    )


@dp.message(lambda m: m.text == "🚀 Автопост")
async def autopost_menu(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    await m.answer(
        "🚀 АВТОПОСТИНГ\n\n"
        f"Статус: {'✅ включен' if AUTOPOST_ENABLED else '❌ выключен'}\n"
        "⏰ Интервал: каждые 3 часа\n\n"
        "/postnow — выложить сейчас\n"
        "/testpost — тест\n"
        "/autostatus — статус"
    )


async def auto_post():
    global AUTOPOST_ENABLED

    if not AUTOPOST_ENABLED:
        print("AUTOPOST OFF")
        return

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
    await m.answer("✅ Готово")


@dp.message(lambda m: m.text == "/testpost")
async def test_post(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return

    text, topic = await generate_text()

    await m.answer(
        f"🧪 ТЕСТ ПОСТА\n\n"
        f"📌 Тема: {topic}\n\n"
        f"{text[:3000]}"
    )


@dp.message(lambda m: m.text == "/autostatus")
async def auto_status(m: types.Message):
    await m.answer(
        f"🚀 Автопостинг: {'✅ включен' if AUTOPOST_ENABLED else '❌ выключен'}\n"
        "⏰ Интервал: 3 часа"
    )


@dp.message(lambda m: m.text == "/autoon")
async def auto_on(m: types.Message):
    global AUTOPOST_ENABLED

    if m.from_user.id != ADMIN_ID:
        return

    AUTOPOST_ENABLED = True
    await m.answer("✅ Автопостинг включен")


@dp.message(lambda m: m.text == "/autooff")
async def auto_off(m: types.Message):
    global AUTOPOST_ENABLED

    if m.from_user.id != ADMIN_ID:
        return

    AUTOPOST_ENABLED = False
    await m.answer("❌ Автопостинг выключен")


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

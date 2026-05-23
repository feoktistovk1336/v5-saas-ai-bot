import asyncio
import os
import random
import aiohttp

from PIL import Image, ImageDraw, ImageFont

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
    LabeledPrice,
    PreCheckoutQuery
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CHANNEL_ID,
    FREE_LIMIT,
    PRO_PRICE_STARS,
    PRO_DAYS,
    BOT_USERNAME
)

from ai import generate_text, generate_carousel
from media import generate_images, generate_reels_text

from db import (
    init_db,
    create_user,
    add_generation,
    get_stats,
    can_generate,
    is_pro,
    set_pro,
    add_payment
)


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


def wrap_text(text, max_chars=14):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = f"{line} {word}".strip()

        if len(test) <= max_chars:
            line = test
        else:
            if line:
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
        except Exception:
            pass

    return ImageFont.load_default()


async def create_ai_image(image_url, title, show_brand=True):
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

        overlay = Image.new("RGBA", image.size, (0, 0, 0, 65))
        image = Image.alpha_composite(image, overlay)

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(55, 545), (1025, 1015)],
            radius=46,
            fill=(0, 0, 0, 215)
        )

        font_big = load_font(76)
        font_small = load_font(34)

        lines = wrap_text(f"🔥 {title.upper()}", 14)

        y = 610
        for index, line in enumerate(lines):
            color = (255, 220, 40) if index == 1 else (255, 255, 255)

            draw.text(
                (90, y),
                line,
                fill=color,
                font=font_big
            )

            y += 86

        draw.text(
            (90, 895),
            "V5 AI SAAS",
            fill=(120, 255, 160),
            font=font_small
        )

        if show_brand:
            draw.rounded_rectangle(
                [(90, 940), (420, 990)],
                radius=25,
                outline=(230, 230, 230),
                width=2
            )

            draw.text(
                (120, 950),
                f"✈ {BOT_USERNAME}",
                fill=(235, 235, 235),
                font=font_small
            )

        image.convert("RGB").save(
            final_file,
            quality=95
        )

        try:
            os.remove(temp_file)
        except Exception:
            pass

        return final_file

    except Exception as e:
        print("CREATE IMAGE ERROR:", e)
        return None


async def user_has_access(user_id):
    if user_id == ADMIN_ID:
        return True

    if await is_pro(user_id):
        return True

    return await can_generate(user_id, FREE_LIMIT)


@dp.message(lambda m: m.text == "/start")
async def start(m: types.Message):
    await create_user(m.from_user.id)

    await m.answer(
        "🚀 Добро пожаловать в PrimeOnix AI\n\n"
        "Создавай AI посты, карусели и Reels за секунды.",
        reply_markup=menu
    )


@dp.message(lambda m: m.text == "🔥 AI Пост")
async def ai_post(m: types.Message):
    try:
        if not await user_has_access(m.from_user.id):
            return await m.answer(
                "❌ Лимит FREE тарифа закончился.\n\n"
                "Оформи PRO в разделе 💳 Тарифы."
            )

        await m.answer("🔥 Создаю AI пост...")

        text, topic = await generate_text()
        images = await generate_images(topic, 1)

        show_brand = not (
            m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id)
        )

        if images:
            final_image = await create_ai_image(
                images[0],
                topic,
                show_brand=show_brand
            )

            if final_image:
                await m.answer_photo(photo=FSInputFile(final_image))

        await m.answer(text[:4000])
        await add_generation(m.from_user.id, "post", text)

    except Exception as e:
        print("AI POST ERROR:", e)
        await m.answer("❌ Ошибка генерации поста")


@dp.message(lambda m: m.text == "🖼 Карусель")
async def carousel(m: types.Message):
    try:
        if not await user_has_access(m.from_user.id):
            return await m.answer(
                "❌ Лимит FREE тарифа закончился.\n\n"
                "Оформи PRO в разделе 💳 Тарифы."
            )

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

        show_brand = not (
            m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id)
        )

        for i, slide in enumerate(slides):
            final_image = await create_ai_image(
                images[i],
                slide,
                show_brand=show_brand
            )

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
        if not await user_has_access(m.from_user.id):
            return await m.answer(
                "❌ Лимит FREE тарифа закончился.\n\n"
                "Оформи PRO в разделе 💳 Тарифы."
            )

        await m.answer("🎬 Создаю Reels...")

        text, topic = await generate_text()
        script = await generate_reels_text(topic)

        await m.answer(f"{script}\n\n{text[:2000]}")
        await add_generation(m.from_user.id, "reels", script)

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
        "🔥 AI SaaS\n"
        "🔥 AI видео\n"
        "🔥 AI маркетинг"
    )


@dp.message(lambda m: m.text == "💳 Тарифы")
async def tariffs(m: types.Message):
    pro = await is_pro(m.from_user.id)

    await m.answer(
        "💎 ТАРИФЫ PRIMEONIX AI\n\n"
        "🆓 FREE\n"
        f"• {FREE_LIMIT} генераций\n"
        "• watermark с ботом\n\n"
        f"🚀 PRO — {PRO_PRICE_STARS} ⭐ / {PRO_DAYS} дней\n"
        "• Безлимит генераций\n"
        "• Без watermark\n"
        "• Автопостинг\n"
        "• Premium AI\n\n"
        f"Твой статус: {'🚀 PRO' if pro else '🆓 FREE'}\n\n"
        "Чтобы оплатить PRO, отправь команду:\n"
        "/buypro"
    )


@dp.message(lambda m: m.text == "/buypro")
async def buy_pro(m: types.Message):
    prices = [
        LabeledPrice(
            label=f"PRO доступ на {PRO_DAYS} дней",
            amount=PRO_PRICE_STARS
        )
    ]

    await bot.send_invoice(
        chat_id=m.chat.id,
        title="PrimeOnix AI PRO",
        description=(
            "Безлимитные AI посты, карусели, Reels и картинки без watermark."
        ),
        payload=f"pro_{m.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices
    )


@dp.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(lambda m: m.successful_payment is not None)
async def successful_payment(m: types.Message):
    payment = m.successful_payment

    await set_pro(m.from_user.id, PRO_DAYS)

    await add_payment(
        m.from_user.id,
        payment.total_amount,
        payment.currency,
        payment.telegram_payment_charge_id
    )

    await m.answer(
        "✅ Оплата прошла успешно!\n\n"
        f"🚀 PRO активирован на {PRO_DAYS} дней."
    )


@dp.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    users, gens, payments = await get_stats()

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n"
        f"💳 Оплат: {payments}\n\n"
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
        "/autostatus — статус\n"
        "/autoon — включить\n"
        "/autooff — выключить"
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
            final_image = await create_ai_image(
                images[0],
                topic,
                show_brand=False
            )

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
    if m.from_user.id != ADMIN_ID:
        return

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

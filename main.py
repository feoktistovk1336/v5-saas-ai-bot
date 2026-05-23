import asyncio
import os
import random
import aiohttp

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
    LabeledPrice,
    PreCheckoutQuery,
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CHANNEL_ID,
    FREE_LIMIT,
    PRO_PRICE_STARS,
    PRO_DAYS,
    BRAND_USERNAME
)

from ai import (
    generate_text,
    generate_carousel,
    generate_content_plan
)

from media import generate_images, generate_reels_text

from db import (
    init_db,
    create_user,
    add_generation,
    get_stats,
    can_generate,
    is_pro,
    set_pro,
    add_payment,
    get_setting,
    set_setting
)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 AI Пост"), KeyboardButton(text="🖼 Карусель")],
        [KeyboardButton(text="🎬 Reels"), KeyboardButton(text="📅 Контент-план")],
        [KeyboardButton(text="🧠 Идеи"), KeyboardButton(text="📈 Тренды")],
        [KeyboardButton(text="💳 Тарифы"), KeyboardButton(text="👑 Админ")],
    ],
    resize_keyboard=True
)


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚀 Пост сейчас", callback_data="admin_postnow"),
            InlineKeyboardButton(text="🧪 Тест поста", callback_data="admin_testpost")
        ],
        [
            InlineKeyboardButton(text="✅ Автопост ON", callback_data="admin_autoon"),
            InlineKeyboardButton(text="❌ Автопост OFF", callback_data="admin_autooff")
        ],
        [
            InlineKeyboardButton(text="⏰ 1 час", callback_data="admin_auto1"),
            InlineKeyboardButton(text="⏰ 3 часа", callback_data="admin_auto3"),
            InlineKeyboardButton(text="⏰ 6 часов", callback_data="admin_auto6")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")
        ]
    ]
)


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


def clean_text(text):
    bad = [
        "🔥", "🚀", "✅", "❌", "💡",
        "1.", "2.", "3.", "4.", "5.",
        "HOOK", "CTA", ":"
    ]

    for item in bad:
        text = text.replace(item, "")

    return text.strip().upper()


def wrap_lines(text, max_chars):
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

    return lines


def fit_title(draw, text, max_width, max_height):
    clean = clean_text(text)

    for size in range(86, 38, -4):
        font = load_font(size)
        max_chars = max(8, int(max_width / (size * 0.58)))
        lines = wrap_lines(clean, max_chars)

        line_height = int(size * 1.08)
        total_height = len(lines) * line_height

        widest = 0

        for line in lines:
            box = draw.textbbox((0, 0), line, font=font)
            widest = max(widest, box[2] - box[0])

        if widest <= max_width and total_height <= max_height:
            return font, lines[:4], line_height

    font = load_font(42)
    return font, wrap_lines(clean, 13)[:4], 48


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

        dark = Image.new("RGBA", image.size, (0, 0, 0, 95))
        image = Image.alpha_composite(image, dark)

        glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)

        for r in range(520, 0, -10):
            alpha = int(90 * (r / 520))
            glow_draw.ellipse(
                [(760 - r, 680 - r), (760 + r, 680 + r)],
                fill=(255, 170, 30, alpha)
            )

        image = Image.alpha_composite(image, glow)

        gradient = Image.new("RGBA", image.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(gradient)

        for yy in range(1080):
            alpha = int(190 * (yy / 1080))
            gd.line([(0, yy), (1080, yy)], fill=(0, 0, 0, alpha))

        image = Image.alpha_composite(image, gradient)

        card_x = 70
        card_y = 145
        card_w = 780
        card_h = 810

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)

        sd.rounded_rectangle(
            [(card_x + 20, card_y + 22), (card_x + card_w + 20, card_y + card_h + 22)],
            radius=60,
            fill=(0, 0, 0, 140)
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(20))
        image = Image.alpha_composite(image, shadow)

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(card_x, card_y), (card_x + card_w, card_y + card_h)],
            radius=60,
            fill=(3, 8, 18, 226),
            outline=(255, 255, 255, 80),
            width=2
        )

        font_badge = load_font(24)
        font_sub = load_font(34)
        font_brand = load_font(25)

        draw.rounded_rectangle(
            [(card_x + 55, card_y + 55), (card_x + 275, card_y + 108)],
            radius=26,
            fill=(255, 255, 255, 22),
            outline=(255, 255, 255, 80),
            width=1
        )

        draw.text(
            (card_x + 83, card_y + 69),
            "AI CREATIVE +",
            fill=(235, 235, 235),
            font=font_badge
        )

        title_font, lines, line_height = fit_title(
            draw,
            title,
            card_w - 120,
            410
        )

        text_y = card_y + 170

        for i, line in enumerate(lines):
            color = (255, 218, 35) if i in [1, 2] else (255, 255, 255)

            draw.text(
                (card_x + 55, text_y),
                line,
                fill=color,
                font=title_font
            )

            text_y += line_height

        subtitle_y = card_y + 545

        draw.text((card_x + 55, subtitle_y), "ТЕХНОЛОГИИ МЕНЯЮТ МИР.", fill=(235, 235, 235), font=font_sub)
        draw.text((card_x + 55, subtitle_y + 48), "ВОПРОС ТОЛЬКО В ТОМ,", fill=(235, 235, 235), font=font_sub)
        draw.text((card_x + 55, subtitle_y + 96), "ИСПОЛЬЗУЕШЬ ЛИ ТЫ ИХ.", fill=(255, 218, 35), font=font_sub)

        draw.rectangle(
            [(card_x + 55, card_y + card_h - 158), (card_x + 175, card_y + card_h - 149)],
            fill=(255, 210, 35)
        )

        draw.text(
            (card_x + 55, card_y + card_h - 110),
            "AI CONTENT",
            fill=(255, 255, 255),
            font=font_sub
        )

        if show_brand:
            badge_x = card_x + 55
            badge_y = card_y + card_h - 62
            badge_w = 330
            badge_h = 46

            draw.rounded_rectangle(
                [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
                radius=23,
                fill=(0, 0, 0, 65),
                outline=(255, 218, 35, 180),
                width=2
            )

            draw.text(
                (badge_x + 28, badge_y + 9),
                BRAND_USERNAME,
                fill=(255, 255, 255),
                font=font_brand
            )

        image.convert("RGB").save(final_file, quality=97)

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


async def is_autopost_enabled():
    value = await get_setting("autopost_enabled", "1")
    return value == "1"


async def get_autopost_hours():
    value = await get_setting("autopost_hours", "3")
    return int(value)


async def setup_autopost_job():
    hours = await get_autopost_hours()

    scheduler.add_job(
        auto_post,
        "interval",
        hours=hours,
        id="autopost",
        replace_existing=True
    )


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
            return await m.answer("❌ Лимит FREE тарифа закончился.\n\nОформи PRO в разделе 💳 Тарифы.")

        await m.answer("🔥 Создаю AI пост...")

        text, topic = await generate_text()
        images = await generate_images(topic, 1)

        show_brand = not (m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id))

        if images:
            final_image = await create_ai_image(images[0], topic, show_brand=show_brand)

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
            return await m.answer("❌ Лимит FREE тарифа закончился.\n\nОформи PRO в разделе 💳 Тарифы.")

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

        show_brand = not (m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id))

        for i, slide in enumerate(slides):
            final_image = await create_ai_image(images[i], slide, show_brand=show_brand)

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
            return await m.answer("❌ Лимит FREE тарифа закончился.\n\nОформи PRO в разделе 💳 Тарифы.")

        await m.answer("🎬 Создаю Reels...")

        text, topic = await generate_text()
        script = await generate_reels_text(topic)

        await m.answer(f"{script}\n\n{text[:2000]}")
        await add_generation(m.from_user.id, "reels", script)

    except Exception as e:
        print("REELS ERROR:", e)
        await m.answer("❌ Ошибка генерации Reels")


@dp.message(lambda m: m.text == "📅 Контент-план")
async def content_plan(m: types.Message):
    try:
        if not await user_has_access(m.from_user.id):
            return await m.answer("❌ Лимит FREE тарифа закончился.\n\nОформи PRO в разделе 💳 Тарифы.")

        await m.answer("📅 Создаю контент-план на 7 дней...")

        plan = await generate_content_plan()

        await m.answer(
            f"📅 КОНТЕНТ-ПЛАН НА 7 ДНЕЙ\n\n{plan}"
        )

        await add_generation(m.from_user.id, "content_plan", plan)

    except Exception as e:
        print("CONTENT PLAN ERROR:", e)
        await m.answer("❌ Ошибка генерации контент-плана")


@dp.message(lambda m: m.text == "🧠 Идеи")
async def ideas(m: types.Message):
    await m.answer(
        "🧠 AI ИДЕИ\n\n"
        "1. 5 AI-инструментов для бизнеса\n"
        "2. Как заработать на нейросетях\n"
        "3. AI vs дизайнеры\n"
        "4. Лучшие GPT для работы\n"
        "5. Как автоматизировать контент"
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
        f"• watermark {BRAND_USERNAME}\n\n"
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
        description="Безлимитные AI посты, карусели, Reels и картинки без watermark.",
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

    await m.answer(f"✅ Оплата прошла успешно!\n\n🚀 PRO активирован на {PRO_DAYS} дней.")


@dp.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    users, gens, payments = await get_stats()
    enabled = await is_autopost_enabled()
    hours = await get_autopost_hours()

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n"
        f"💳 Оплат: {payments}\n"
        f"🚀 Автопост: {'ON' if enabled else 'OFF'}\n"
        f"⏰ Интервал: {hours} ч.",
        reply_markup=admin_panel
    )


@dp.message(lambda m: m.text == "🚀 Автопост")
async def autopost_menu(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    enabled = await is_autopost_enabled()
    hours = await get_autopost_hours()

    await m.answer(
        "🚀 АВТОПОСТИНГ\n\n"
        f"Статус: {'✅ включен' if enabled else '❌ выключен'}\n"
        f"⏰ Интервал: {hours} ч.",
        reply_markup=admin_panel
    )


@dp.callback_query(lambda c: c.data == "admin_stats")
async def cb_admin_stats(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    users, gens, payments = await get_stats()
    enabled = await is_autopost_enabled()
    hours = await get_autopost_hours()

    await c.message.answer(
        "📊 СТАТИСТИКА\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n"
        f"💳 Оплат: {payments}\n"
        f"🚀 Автопост: {'ON' if enabled else 'OFF'}\n"
        f"⏰ Интервал: {hours} ч."
    )

    await c.answer()


@dp.callback_query(lambda c: c.data == "admin_postnow")
async def cb_post_now(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await c.message.answer("🚀 Публикую пост...")
    await auto_post()
    await c.message.answer("✅ Пост опубликован")
    await c.answer()


@dp.callback_query(lambda c: c.data == "admin_testpost")
async def cb_test_post(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    text, topic = await generate_text()

    await c.message.answer(
        f"🧪 ТЕСТ ПОСТА\n\n"
        f"📌 Тема: {topic}\n\n"
        f"{text[:3000]}"
    )

    await c.answer()


@dp.callback_query(lambda c: c.data == "admin_autoon")
async def cb_auto_on(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await set_setting("autopost_enabled", "1")
    await c.message.answer("✅ Автопостинг включен")
    await c.answer()


@dp.callback_query(lambda c: c.data == "admin_autooff")
async def cb_auto_off(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await set_setting("autopost_enabled", "0")
    await c.message.answer("❌ Автопостинг выключен")
    await c.answer()


@dp.callback_query(lambda c: c.data in ["admin_auto1", "admin_auto3", "admin_auto6"])
async def cb_auto_interval(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    hours = int(c.data.replace("admin_auto", ""))

    await set_setting("autopost_hours", str(hours))
    await setup_autopost_job()

    await c.message.answer(f"✅ Интервал автопостинга изменен: {hours} ч.")
    await c.answer()


async def auto_post():
    if not await is_autopost_enabled():
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


async def on_startup():
    await init_db()

    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(
        [
            BotCommand(
                command="start",
                description="Запуск бота"
            )
        ]
    )

    await setup_autopost_job()

    scheduler.start()

    print("БОТ ЗАПУЩЕН")


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InputMediaPhoto
)

from config import BOT_TOKEN, CHANNEL_ID, ADMIN_ID
from ai import generate_text
from media import generate_images
from db import init_db, create_user, get_user


# ================= FASTAPI =================
app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


# ================= BOT =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ================= MENU =================
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 AI Post")],
        [KeyboardButton(text="🎬 Reels")],
        [KeyboardButton(text="🖼 Carousel")],
        [KeyboardButton(text="💳 Upgrade")],
        [KeyboardButton(text="👑 Admin")]
    ],
    resize_keyboard=True
)


# ================= START =================
@dp.message()
async def start(m: types.Message):
    await create_user(m.from_user.id)
    await m.answer("🚀 V5 SaaS ready", reply_markup=menu)


# ================= AI POST =================
@dp.message(lambda m: m.text == "🔥 AI Post")
async def ai_post(m: types.Message):
    text, topic = await generate_text()
    await m.answer(text)


# ================= CAROUSEL =================
@dp.message(lambda m: m.text == "🖼 Carousel")
async def carousel(m: types.Message):
    text, topic = await generate_text()

    images = await generate_images(topic, 5)

    media = [
        InputMediaPhoto(media=img)
        for img in images
    ]

    await bot.send_media_group(
        chat_id=m.chat.id,
        media=media
    )

    await m.answer(text)


# ================= REELS =================
@dp.message(lambda m: m.text == "🎬 Reels")
async def reels(m: types.Message):
    text, topic = await generate_text()

    script = f"🎬 REELS:\n\n{topic}\n\n{text}"

    await m.answer(script)


# ================= ADMIN =================
@dp.message(lambda m: m.text == "👑 Admin")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ no access")

    await m.answer(
        "👑 ADMIN PANEL\n\n"
        "/users - list users\n"
        "/stats - system stats"
    )


# ================= STARTUP =================
@app.on_event("startup")
async def startup():
    await init_db()

    asyncio.create_task(
        dp.start_polling(bot)
    )


# ================= SHUTDOWN =================
@app.on_event("shutdown")
async def shutdown():
    await bot.session.close()

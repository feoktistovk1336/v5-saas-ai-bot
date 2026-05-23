from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from services.ai_service import rewrite_text
from database.db import add_generation

router = Router()

rewrite_mode = {}
rewrite_waiting = {}


@router.message(lambda m: m.text == "✍️ Rewrite")
async def rewrite_menu(m: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔥 Viral", callback_data="rw_viral"),
                InlineKeyboardButton(text="💎 Luxury", callback_data="rw_luxury")
            ],
            [
                InlineKeyboardButton(text="⚡ Aggressive", callback_data="rw_aggressive"),
                InlineKeyboardButton(text="🎬 Reels", callback_data="rw_reels")
            ],
            [
                InlineKeyboardButton(text="📱 Telegram", callback_data="rw_telegram")
            ]
        ]
    )

    await m.answer(
        "✍️ Выбери стиль rewrite:",
        reply_markup=kb
    )


@router.callback_query(lambda c: c.data.startswith("rw_"))
async def rewrite_style(c: CallbackQuery):
    style = c.data.replace("rw_", "")

    rewrite_mode[c.from_user.id] = style
    rewrite_waiting[c.from_user.id] = True

    await c.message.answer("📩 Отправь текст для переписывания.")
    await c.answer()


@router.message()
async def rewrite_handler(m: types.Message):
    if not rewrite_waiting.get(m.from_user.id):
        return

    rewrite_waiting[m.from_user.id] = False

    style = rewrite_mode.get(m.from_user.id, "viral")

    await m.answer("✍️ Переписываю...")

    result = await rewrite_text(m.text, style)

    await m.answer(result[:4000])

    await add_generation(m.from_user.id, "rewrite", result[:1000])

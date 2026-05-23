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
                InlineKeyboardButton(text="🔥 Вирусно", callback_data="rw_viral"),
                InlineKeyboardButton(text="💎 Дорого", callback_data="rw_luxury")
            ],
            [
                InlineKeyboardButton(text="⚡ Продающе", callback_data="rw_aggressive"),
                InlineKeyboardButton(text="🎬 Reels", callback_data="rw_reels")
            ],
            [
                InlineKeyboardButton(text="📱 Telegram-пост", callback_data="rw_telegram")
            ]
        ]
    )

    await m.answer(
        "✍️ <b>Rewrite</b>\n\n"
        "Выбери стиль переписывания:",
        reply_markup=kb
    )


@router.callback_query(lambda c: c.data.startswith("rw_"))
async def rewrite_style(c: CallbackQuery):
    style = c.data.replace("rw_", "")

    rewrite_mode[c.from_user.id] = style
    rewrite_waiting[c.from_user.id] = True

    await c.message.answer(
        "📩 Теперь отправь текст, который нужно переписать."
    )

    await c.answer()


@router.message(lambda m: rewrite_waiting.get(m.from_user.id, False))
async def rewrite_handler(m: types.Message):
    rewrite_waiting[m.from_user.id] = False

    style = rewrite_mode.get(m.from_user.id, "viral")

    await m.answer("✍️ Переписываю текст...")

    result = await rewrite_text(m.text, style)

    await m.answer(result[:4000])

    await add_generation(
        m.from_user.id,
        "rewrite",
        result[:1000]
    )

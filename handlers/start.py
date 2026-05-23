from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database.db import create_user

router = Router()


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📦 Контент"),
            KeyboardButton(text="✍️ Rewrite")
        ],
        [
            KeyboardButton(text="🧬 Бренд-стиль"),
            KeyboardButton(text="💎 PRO")
        ],
        [
            KeyboardButton(text="👑 Админ")
        ]
    ],
    resize_keyboard=True
)


content_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔥 AI Пост"),
            KeyboardButton(text="🖼 Карусель")
        ],
        [
            KeyboardButton(text="🎬 Reels"),
            KeyboardButton(text="📅 Контент-план")
        ],
        [
            KeyboardButton(text="🏭 Контент-завод")
        ],
        [
            KeyboardButton(text="🧠 Идеи"),
            KeyboardButton(text="📈 Тренды")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def start(m: types.Message):
    await create_user(m.from_user.id)

    await m.answer(
        "🚀 <b>PrimeOnix AI</b>\n\n"
        "AI SaaS платформа для постов, каруселей, Reels и контент-планов.",
        reply_markup=main_menu
    )


@router.message(lambda m: m.text == "📦 Контент")
async def open_content(m: types.Message):
    await m.answer(
        "📦 <b>Раздел контента</b>",
        reply_markup=content_menu
    )


@router.message(lambda m: m.text == "⬅️ Назад")
async def back(m: types.Message):
    await m.answer(
        "🏠 Главное меню",
        reply_markup=main_menu
    )

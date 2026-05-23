from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import ADMIN_ID
from database.db import get_stats, get_setting, set_setting
from services.autopost_service import auto_post

router = Router()


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚀 Пост сейчас", callback_data="admin_postnow"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton(text="✅ Автопост ON", callback_data="admin_autoon"),
            InlineKeyboardButton(text="❌ Автопост OFF", callback_data="admin_autooff")
        ]
    ]
)


async def is_autopost_enabled():
    return await get_setting("autopost_enabled", "1") == "1"


@router.message(lambda m: m.text == "👑 Админ")
async def admin(m: types.Message):
    if m.from_user.id != ADMIN_ID:
        return await m.answer("❌ Нет доступа")

    users, gens, payments = await get_stats()
    enabled = await is_autopost_enabled()

    await m.answer(
        "👑 <b>ADMIN PANEL</b>\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n"
        f"💳 Оплат: {payments}\n"
        f"🚀 Автопост: {'ON' if enabled else 'OFF'}",
        reply_markup=admin_panel
    )


@router.callback_query(lambda c: c.data == "admin_stats")
async def stats(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    users, gens, payments = await get_stats()

    await c.message.answer(
        "📊 <b>СТАТИСТИКА</b>\n\n"
        f"👥 Пользователей: {users}\n"
        f"🧠 Генераций: {gens}\n"
        f"💳 Оплат: {payments}"
    )

    await c.answer()


@router.callback_query(lambda c: c.data == "admin_postnow")
async def post_now(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await c.message.answer("🚀 Публикую пост...")
    await auto_post(c.bot)
    await c.message.answer("✅ Готово")
    await c.answer()


@router.callback_query(lambda c: c.data == "admin_autoon")
async def auto_on(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await set_setting("autopost_enabled", "1")
    await c.message.answer("✅ Автопостинг включен")
    await c.answer()


@router.callback_query(lambda c: c.data == "admin_autooff")
async def auto_off(c: CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        return await c.answer("Нет доступа", show_alert=True)

    await set_setting("autopost_enabled", "0")
    await c.message.answer("❌ Автопостинг выключен")
    await c.answer()

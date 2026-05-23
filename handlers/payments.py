from aiogram import Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery

from config import PRO_PRICE_STARS, PRO_DAYS, BRAND_USERNAME
from database.db import is_pro, set_pro, add_payment

router = Router()


@router.message(lambda m: m.text == "💎 PRO")
async def pro_menu(m: types.Message):
    pro = await is_pro(m.from_user.id)

    await m.answer(
        "💎 <b>PRIMEONIX AI PRO</b>\n\n"
        "🆓 FREE:\n"
        "• 5 генераций\n"
        f"• watermark {BRAND_USERNAME}\n\n"
        f"🚀 PRO — {PRO_PRICE_STARS} ⭐ / {PRO_DAYS} дней\n"
        "• Безлимит генераций\n"
        "• Без watermark\n"
        "• Premium AI visuals\n"
        "• Content Factory\n"
        "• Rewrite\n\n"
        f"Твой статус: {'🚀 PRO' if pro else '🆓 FREE'}\n\n"
        "Для оплаты отправь /buypro"
    )


@router.message(lambda m: m.text == "/buypro")
async def buy_pro(m: types.Message):
    prices = [
        LabeledPrice(
            label=f"PRO на {PRO_DAYS} дней",
            amount=PRO_PRICE_STARS
        )
    ]

    await m.bot.send_invoice(
        chat_id=m.chat.id,
        title="PrimeOnix AI PRO",
        description="Безлимитные AI генерации и premium visuals.",
        payload=f"pro_{m.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices
    )


@router.pre_checkout_query()
async def pre_checkout(q: PreCheckoutQuery):
    await q.answer(ok=True)


@router.message(lambda m: m.successful_payment is not None)
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
        f"✅ Оплата прошла успешно!\n\n🚀 PRO активирован на {PRO_DAYS} дней."
    )

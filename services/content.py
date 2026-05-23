import random

from aiogram import Router, types
from aiogram.types import FSInputFile

from config import ADMIN_ID, FREE_LIMIT
from database.db import can_generate, is_pro, add_generation

from services.ai_service import (
    generate_post,
    generate_carousel,
    generate_reels_text,
    generate_content_plan,
    generate_content_factory
)

from services.image_service import (
    generate_ai_background,
    create_poster
)

router = Router()


async def user_has_access(user_id):
    if user_id == ADMIN_ID:
        return True

    if await is_pro(user_id):
        return True

    return await can_generate(user_id, FREE_LIMIT)


@router.message(lambda m: m.text == "🔥 AI Пост")
async def ai_post(m: types.Message):
    if not await user_has_access(m.from_user.id):
        return await m.answer("❌ Лимит FREE закончился. Оформи PRO.")

    await m.answer("🔥 Создаю AI пост...")

    text, visual_title = await generate_post()

    show_brand = not (
        m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id)
    )

    bg = await generate_ai_background(visual_title)
    poster = await create_poster(bg, visual_title, show_brand)

    if poster:
        await m.answer_photo(photo=FSInputFile(poster))

    await m.answer(text[:4000])

    await add_generation(m.from_user.id, "post", text)


@router.message(lambda m: m.text == "🖼 Карусель")
async def carousel(m: types.Message):
    if not await user_has_access(m.from_user.id):
        return await m.answer("❌ Лимит FREE закончился. Оформи PRO.")

    await m.answer("🖼 Создаю AI карусель...")

    topic = random.choice([
        "AI бизнес",
        "нейросети",
        "AI маркетинг",
        "AI стартапы",
        "AI контент"
    ])

    slides = await generate_carousel(topic)

    show_brand = not (
        m.from_user.id == ADMIN_ID or await is_pro(m.from_user.id)
    )

    for slide in slides:
        bg = await generate_ai_background(slide)
        poster = await create_poster(bg, slide, show_brand)

        if poster:
            await m.answer_photo(photo=FSInputFile(poster))

    await add_generation(m.from_user.id, "carousel", topic)

    await m.answer("🔥 AI карусель готова")


@router.message(lambda m: m.text == "🎬 Reels")
async def reels(m: types.Message):
    if not await user_has_access(m.from_user.id):
        return await m.answer("❌ Лимит FREE закончился. Оформи PRO.")

    await m.answer("🎬 Создаю Reels...")

    script = await generate_reels_text("AI контент")

    await m.answer(script[:4000])

    await add_generation(m.from_user.id, "reels", script)


@router.message(lambda m: m.text == "📅 Контент-план")
async def content_plan(m: types.Message):
    if not await user_has_access(m.from_user.id):
        return await m.answer("❌ Лимит FREE закончился. Оформи PRO.")

    await m.answer("📅 Создаю контент-план...")

    plan = await generate_content_plan()

    await m.answer(plan[:4000])

    await add_generation(m.from_user.id, "content_plan", plan)


@router.message(lambda m: m.text == "🏭 Контент-завод")
async def factory(m: types.Message):
    if not await user_has_access(m.from_user.id):
        return await m.answer("❌ Лимит FREE закончился. Оформи PRO.")

    await m.answer("🏭 Создаю Content Factory...")

    result = await generate_content_factory()

    for i in range(0, len(result), 4000):
        await m.answer(result[i:i + 4000])

    await add_generation(m.from_user.id, "factory", result[:1000])


@router.message(lambda m: m.text == "🧠 Идеи")
async def ideas(m: types.Message):
    await m.answer(
        "🧠 AI ИДЕИ\n\n"
        "1. AI для бизнеса\n"
        "2. Нейросети для Instagram\n"
        "3. Как заработать на AI\n"
        "4. AI автоматизация\n"
        "5. AI SaaS за 30 дней"
    )


@router.message(lambda m: m.text == "📈 Тренды")
async def trends(m: types.Message):
    await m.answer(
        "📈 AI ТРЕНДЫ\n\n"
        "🔥 AI агенты\n"
        "🔥 AI видео\n"
        "🔥 Faceless YouTube\n"
        "🔥 AI SaaS\n"
        "🔥 Автоматизация контента"
    )

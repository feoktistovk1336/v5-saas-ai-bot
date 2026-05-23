from aiogram.types import FSInputFile

from config import CHANNEL_ID
from database.db import get_setting
from services.ai_service import generate_post
from services.image_service import generate_ai_background, create_poster


async def auto_post(bot):
    enabled = await get_setting("autopost_enabled", "1")

    if enabled != "1":
        print("AUTOPOST OFF")
        return

    try:
        text, title = await generate_post()

        bg = await generate_ai_background(title)
        poster = await create_poster(bg, title, show_brand=False)

        if poster:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=FSInputFile(poster)
            )

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text[:4000]
        )

        print("AUTOPOST SUCCESS")

    except Exception as e:
        print("AUTOPOST ERROR:", e)

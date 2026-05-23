import aiohttp
import os
import random

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from aiogram.types import FSInputFile


# ================= STYLES =================
COLORS = [
    (15, 15, 15),
    (25, 25, 112),
    (45, 45, 45),
    (70, 20, 90),
    (0, 0, 0)
]


# ================= IMAGE GENERATION =================
async def generate_images(prompt: str, count=5):

    images = []

    os.makedirs("temp", exist_ok=True)

    async with aiohttp.ClientSession() as session:

        for i in range(count):

            seed = random.randint(1, 999999)

            url = (
    f"https://image.pollinations.ai/prompt/"
    f"beautiful%20{prompt}%20ai%20art"
    f"?width=1024&height=1024&seed={seed}&model=flux"
)

            try:

                async with session.get(url) as r:

                    filename = f"temp/{i}.jpg"

                    if r.status == 200:

                        with open(filename, "wb") as f:
                            f.write(await r.read())

                        # ================= OPEN IMAGE =================
                        img = Image.open(filename)

                        img = img.resize((1080, 1080))

                        # ================= OVERLAY =================
                        overlay = Image.new(
                            "RGBA",
                            img.size,
                            (*random.choice(COLORS), 120)
                        )

                        img = Image.alpha_composite(
                            img.convert("RGBA"),
                            overlay
                        )

                        draw = ImageDraw.Draw(img)

                        # ================= TEXT =================
                        text = prompt.upper()[:40]

                        try:
                            font = ImageFont.truetype(
                                "arial.ttf",
                                60
                            )
                        except:
                            font = ImageFont.load_default()

                        draw.text(
                            (60, 120),
                            text,
                            fill="white",
                            font=font
                        )

                        # ================= BRAND =================
                        draw.text(
                            (60, 950),
                            "V5 AI SAAS",
                            fill="white",
                            font=font
                        )

                        img = img.convert("RGB")

                        img.save(filename)

                        images.append(
                            FSInputFile(filename)
                        )

                    else:

                        print("IMAGE STATUS:", r.status)

            except Exception as e:

                print("IMAGE ERROR:", e)

    return images


# ================= REELS =================
async def generate_reels_text(topic: str):

    return f"""
🎬 AI REELS

🔥 Тема:
{topic}

🚀 Подпишись на V5 AI SaaS
"""

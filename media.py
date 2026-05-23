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


import random


STYLES = [

    "AI futuristic",
    "cyberpunk",
    "minimal tech",
    "startup branding",
    "dark neon"

]


# ================= GENERATE IMAGES =================
async def generate_images(topic, count=5):

    images = []

    for i in range(count):

        style = random.choice(STYLES)

        seed = random.randint(1, 999999)

        prompt = f"""
        {topic},
        modern AI design,
        social media style,
        viral content,
        {style}
        """

        url = (
            f"https://image.pollinations.ai/prompt/"
            f"{prompt}?seed={seed}"
        )

        images.append(url)

    return images
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

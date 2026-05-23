import random
import aiohttp
import replicate

from config import REPLICATE_API_TOKEN


replicate_client = replicate.Client(
    api_token=REPLICATE_API_TOKEN
)


AI_STYLES = [
    "luxury ai marketing poster",
    "futuristic cyberpunk ai art",
    "premium saas advertising visual",
    "dark cinematic ai concept",
    "glowing neural network aesthetic",
    "luxury tech branding visual",
    "modern ai startup poster",
    "artificial intelligence future concept",
    "ultra realistic ai visual",
    "high-end futuristic digital art"
]


async def generate_images(topic, count=1):

    images = []

    try:

        for _ in range(count):

            style = random.choice(AI_STYLES)

            prompt = f"""
{style},
{topic},
orange cinematic glow,
dark premium background,
high contrast,
luxury futuristic lighting,
instagram premium creative,
viral marketing visual,
modern ai startup design,
depth,
cinematic atmosphere,
ultra detailed,
8k
"""

            output = replicate_client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "go_fast": True,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "jpg",
                    "output_quality": 95
                }
            )

            if output and len(output) > 0:
                images.append(output[0])

        return images

    except Exception as e:
        print("REPLICATE ERROR:", e)

        return [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&q=95"
        ] * count


async def generate_reels_text(topic):

    hooks = [
        "95% людей используют AI неправильно",
        "AI уже заменяет сотрудников",
        "Этот AI инструмент меняет всё",
        "Ты теряешь время без AI",
        "Будущее уже наступило"
    ]

    hook = random.choice(hooks)

    return f"""
🎬 REELS SCRIPT

🎯 Хук:
{hook}

📌 Тема:
{topic}

📹 Сценарий:
1. Мощный хук
2. Боль аудитории
3. Как AI решает проблему
4. Пример результата
5. CTA подписаться

🚀 CTA:
Подпишись на @primeonix26
"""

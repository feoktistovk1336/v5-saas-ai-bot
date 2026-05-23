import random


AI_BACKGROUNDS = [
    "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1080&q=95",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&q=95",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1080&q=95",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1080&q=95",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&q=95",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1080&q=95",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1080&q=95",
    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1080&q=95",
    "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1080&q=95",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&q=95",
    "https://images.unsplash.com/photo-1557683316-973673baf926?w=1080&q=95",
    "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1080&q=95"
]


async def generate_images(topic, count=5):
    return random.sample(
        AI_BACKGROUNDS,
        min(count, len(AI_BACKGROUNDS))
    )


async def generate_reels_text(topic):
    return f"""
🎬 REELS SCRIPT

📌 Тема:
{topic}

🧠 Сценарий:
1. Первые 2 секунды — сильный хук.
2. Покажи боль аудитории.
3. Покажи, как AI решает проблему.
4. Дай пример результата.
5. Заверши призывом подписаться.

🚀 CTA:
Подпишись на @primeonix26 для новых AI идей.
"""

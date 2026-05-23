import random


AI_BACKGROUNDS = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1080&q=90",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1080&q=90",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&q=90",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1080&q=90",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&q=90",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1080&q=90",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080&q=90",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1080&q=90",
    "https://images.unsplash.com/photo-1557683316-973673baf926?w=1080&q=90",
    "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1080&q=90"
]


async def generate_images(topic, count=5):
    if count <= len(AI_BACKGROUNDS):
        return random.sample(AI_BACKGROUNDS, count)

    return [
        random.choice(AI_BACKGROUNDS)
        for _ in range(count)
    ]


async def generate_reels_text(topic):
    return f"""
🎬 REELS SCRIPT

📌 Тема:
{topic}

🧠 Сценарий:
1. Зацепи внимание.
2. Покажи проблему.
3. Дай AI-решение.
4. Покажи результат.
5. Заверши CTA.

🚀 CTA:
Подпишись для новых AI идей.
"""

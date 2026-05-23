import random


AI_IMAGES = [

    "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080",
    "https://images.unsplash.com/photo-1674027392884-7515e76d7d24?w=1080",
    "https://images.unsplash.com/photo-1676299081847-824916de030a?w=1080",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1080",
    "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1080",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1080",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1080",
    "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1080",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1080"

]


async def generate_images(topic, count=5):
    images = random.sample(
        AI_IMAGES,
        min(count, len(AI_IMAGES))
    )

    return images


async def generate_reels_text(topic):
    hooks = [
        "Ты не готов к этому",
        "AI уже меняет рынок",
        "Большинство не знает этого",
        "Это будущее контента",
        "Нейросети захватывают интернет"
    ]

    hook = random.choice(hooks)

    return f"""
🎬 REELS

🔥 Хук:
{hook}

📌 Тема:
{topic}

🧠 Сценарий:
1. Зацепи внимание в первые 2 секунды.
2. Покажи проблему.
3. Дай AI-решение.
4. Заверши сильным призывом.

🚀 CTA:
Подпишись для новых AI идей.
"""

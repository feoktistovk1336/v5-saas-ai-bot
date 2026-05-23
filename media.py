import random


AI_IMAGES = [
    "https://picsum.photos/900/900?1",
    "https://picsum.photos/900/900?2",
    "https://picsum.photos/900/900?3",
    "https://picsum.photos/900/900?4",
    "https://picsum.photos/900/900?5",
    "https://picsum.photos/900/900?6",
    "https://picsum.photos/900/900?7",
    "https://picsum.photos/900/900?8",
    "https://picsum.photos/900/900?9",
    "https://picsum.photos/900/900?10"
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

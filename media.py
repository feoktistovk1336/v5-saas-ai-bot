import random


async def generate_images(topic, count=5):
    images = []

    for _ in range(count):
        seed = random.randint(1, 99999999)

        url = (
            f"https://picsum.photos/seed/{seed}/1080/1080"
        )

        images.append(url)

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

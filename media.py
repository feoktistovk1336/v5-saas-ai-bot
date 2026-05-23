import random


AI_IMAGES = [

    "https://images.unsplash.com/photo-1677442136019-21780ecad995",
    "https://images.unsplash.com/photo-1674027392884-7515e76d7d24",
    "https://images.unsplash.com/photo-1676299081847-824916de030a",
    "https://images.unsplash.com/photo-1675557009875-436f2f7a3d18",
    "https://images.unsplash.com/photo-1677442135703-1787eea5ce01",
    "https://images.unsplash.com/photo-1686191128892-3b8d6f840a52",
    "https://images.unsplash.com/photo-1677442135722-5f0c7a7d2d88"

]


# ================= GENERATE IMAGES =================
async def generate_images(topic, count=5):

    images = []

    for i in range(count):

        image = random.choice(AI_IMAGES)

        images.append(image)

    return images


# ================= REELS =================
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

🚀 Подпишись для новых AI идей.
"""

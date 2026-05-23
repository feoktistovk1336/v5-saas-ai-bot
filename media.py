import random


# ================= AI IMAGES =================
AI_IMAGES = [

    "https://picsum.photos/900/900?1",
    "https://picsum.photos/900/900?2",
    "https://picsum.photos/900/900?3",
    "https://picsum.photos/900/900?4",
    "https://picsum.photos/900/900?5",
    "https://picsum.photos/900/900?6",
    "https://picsum.photos/900/900?7",
    "https://picsum.photos/900/900?8"

]


# ================= GENERATE IMAGES =================
async def generate_images(topic, count=5):

    unique_images = random.sample(
        AI_IMAGES,
        min(count, len(AI_IMAGES))
    )

    return unique_images


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

import random


# ================= STYLES =================
STYLES = [

    "cyberpunk",
    "futuristic AI",
    "dark neon",
    "startup branding",
    "viral instagram style",
    "modern digital art",
    "AI social media",
    "minimal tech",
    "luxury tech",
    "futuristic business"

]


# ================= GENERATE IMAGES =================
async def generate_images(topic, count=5):

    images = []

    for i in range(count):

        style = random.choice(STYLES)

        seed = random.randint(
            1,
            9999999
        )

        # короткий prompt = стабильнее
        prompt = (
            f"{topic}, "
            f"{style}, "
            f"instagram carousel, "
            f"digital art"
        )

        url = (
            "https://image.pollinations.ai/prompt/"
            f"{prompt}"
            f"?seed={seed}"
            f"&width=1024"
            f"&height=1024"
        )

        images.append(url)

    return images


# ================= REELS TEXT =================
async def generate_reels_text(topic):

    hooks = [

        "Ты не готов к этому",
        "AI уже меняет рынок",
        "Большинство не знает этого",
        "Это будущее контента",
        "Нейросети захватывают интернет"

    ]

    hook = random.choice(hooks)

    text = f"""
🎬 REELS

🔥 Хук:
{hook}

📌 Тема:
{topic}

🧠 Сценарий:
Расскажи проблему.
Покажи AI решение.
Добавь вау-эффект.
Сделай сильный CTA.

🚀 CTA:
Подпишись для новых AI идей.
"""

    return text

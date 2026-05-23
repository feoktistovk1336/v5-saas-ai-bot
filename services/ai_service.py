import random
import aiohttp

from config import GROQ_API_KEY


VISUAL_HOOKS = [
    "AI ОТКРЫВАЕТ НОВЫЕ ВОЗМОЖНОСТИ",
    "AI МЕНЯЕТ ПРАВИЛА ИГРЫ",
    "БУДУЩЕЕ СОЗДАЮТ ТЕ, КТО ДЕЙСТВУЕТ",
    "НЕЙРОСЕТИ — НОВАЯ НЕФТЬ",
    "AI ДЕЛАЕТ БИЗНЕС БЫСТРЕЕ",
    "АВТОМАТИЗИРУЙ СЕЙЧАС"
]


TOPICS = [
    "AI бизнес",
    "нейросети",
    "AI маркетинг",
    "автоматизация",
    "AI контент",
    "заработок на AI"
]


async def ask_groq(prompt, max_tokens=900):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1.15,
        "max_tokens": max_tokens
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            data = await response.json()

            if "choices" not in data:
                print("GROQ ERROR:", data)
                return None

            return data["choices"][0]["message"]["content"]


async def generate_post():
    topic = random.choice(TOPICS)
    visual_title = random.choice(VISUAL_HOOKS)

    prompt = f"""
Напиши мощный Telegram-пост на русском.

Тема:
{topic}

Визуальный заголовок:
{visual_title}

Стиль:
— viral
— короткие абзацы
— без воды
— AI creator / SaaS founder
— продающе
— удержание внимания

Структура:
1. Hook
2. Боль
3. Почему старые методы умирают
4. AI решение
5. CTA подписаться
"""

    text = await ask_groq(prompt, 900)

    if not text:
        text = "AI меняет рынок прямо сейчас. Кто действует сегодня — получает преимущество завтра."

    return text[:3500], visual_title


async def generate_carousel(topic="AI бизнес"):
    prompt = f"""
Создай 5 слайдов для дорогой AI/SaaS Instagram-карусели.

Тема:
{topic}

Только 5 строк.
Каждая строка — один слайд.
Максимум 5 слов.
Стиль: мощно, дорого, viral, caps lock.
"""

    text = await ask_groq(prompt, 300)

    if not text:
        return [
            "AI МЕНЯЕТ ПРАВИЛА",
            "СТАРЫЕ МЕТОДЫ УМИРАЮТ",
            "АВТОМАТИЗИРУЙ СЕЙЧАС",
            "ВЫИГРЫВАЙ ВРЕМЯ",
            "НАЧНИ ПРЯМО СЕЙЧАС"
        ]

    slides = []

    for line in text.split("\n"):
        line = (
            line.strip()
            .replace("1.", "")
            .replace("2.", "")
            .replace("3.", "")
            .replace("4.", "")
            .replace("5.", "")
            .replace("-", "")
            .replace("•", "")
            .strip()
            .upper()
        )

        if line:
            slides.append(line)

    return slides[:5]


async def generate_content_plan():
    prompt = """
Создай контент-план на 7 дней для Telegram-канала про AI.

Формат:

День 1:
Пост:
Карусель:
Reels:

До дня 7.

Стиль: AI, бизнес, автоматизация, продажи, creator economy.
"""

    text = await ask_groq(prompt, 1200)

    return text[:4000] if text else "Не удалось создать контент-план."


async def generate_content_factory():
    prompt = """
Создай AI Content Factory Pack.

Нужно:
1. 10 VIRAL HOOKS
2. 10 AI POST IDEAS
3. 10 REELS IDEAS
4. 10 CAROUSEL IDEAS
5. 10 CTA

Тематика:
AI, нейросети, автоматизация, AI бизнес, AI маркетинг.

Стиль:
дорого, viral, коротко, эмоционально, aggressive marketing.
"""

    text = await ask_groq(prompt, 1800)

    return text[:12000] if text else "Не удалось создать контент-завод."


async def rewrite_text(text, style="viral"):
    styles = {
        "viral": "сделай максимально вирусно и эмоционально",
        "luxury": "сделай дорого, premium, luxury marketing",
        "aggressive": "сделай агрессивно и продающе",
        "reels": "сделай как сценарий Reels",
        "telegram": "сделай как viral Telegram пост"
    }

    prompt = f"""
Перепиши текст.

Стиль:
{styles.get(style, styles["viral"])}

Правила:
— короткие абзацы
— сильный hook
— без воды
— современно
— удерживает внимание

Текст:
{text}
"""

    result = await ask_groq(prompt, 1000)

    return result[:4000] if result else "Не удалось переписать текст."


async def generate_reels_text(topic):
    prompt = f"""
Создай короткий Reels script на русском.

Тема:
{topic}

Формат:
Хук:
Сценарий:
CTA:

Стиль: AI creator, short video, viral.
"""

    text = await ask_groq(prompt, 600)

    return text[:3000] if text else "Не удалось создать Reels."

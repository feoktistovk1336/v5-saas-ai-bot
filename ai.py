import aiohttp
import random

from config import GROQ_API_KEY
from topics import TOPICS


VISUAL_HOOKS = [
    "AI ОТКРЫВАЕТ НОВЫЕ ВОЗМОЖНОСТИ",
    "AI МЕНЯЕТ ПРАВИЛА ИГРЫ",
    "БУДУЩЕЕ СОЗДАЮТ ТЕ, КТО ДЕЙСТВУЕТ",
    "НЕЙРОСЕТИ — НОВАЯ НЕФТЬ",
    "AI ДЕЛАЕТ БИЗНЕС БЫСТРЕЕ",
    "АВТОМАТИЗИРУЙ СЕЙЧАС — ВЫИГРЫВАЙ ЗАВТРА",
    "КОНТЕНТ БОЛЬШЕ НЕ ДЕЛАЮТ ВРУЧНУЮ",
    "AI УЖЕ ЗДЕСЬ. ВОПРОС: ТЫ ГОТОВ?"
]


REWRITE_STYLES = {
    "viral": "сделай максимально вирусно, дерзко, эмоционально",
    "luxury": "сделай дорого, premium style, luxury marketing",
    "aggressive": "сделай агрессивно и продающе",
    "reels": "сделай как сценарий reels",
    "telegram": "сделай как viral telegram post"
}


async def ask_groq(prompt, max_tokens=700):

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


async def generate_text():

    category = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[category])
    visual_title = random.choice(VISUAL_HOOKS)

    prompt = f"""
Напиши мощный Telegram-пост.

Тема:
{topic}

Главная идея:
{visual_title}

Стиль:
— современно
— viral
— дорого
— AI creator style
— короткие абзацы
— удержание внимания
— эмоционально
— продающе

Структура:
1. Hook
2. Боль
3. Почему старые методы умирают
4. Как AI решает проблему
5. CTA

Не пиши скучно.
"""

    try:

        text = await ask_groq(prompt, 800)

        if not text:
            return (
                "AI меняет рынок прямо сейчас.",
                visual_title
            )

        return text[:3500], visual_title

    except Exception as e:

        print("AI ERROR:", e)

        return (
            "AI меняет рынок прямо сейчас.",
            visual_title
        )


async def generate_carousel(topic):

    prompt = f"""
Создай 5 ultra viral слайдов.

Тема:
{topic}

Формат:
5 коротких строк.

Стиль:
— дорого
— мощно
— luxury
— как AI SaaS
— максимум 5 слов
— caps lock

Без пояснений.
"""

    try:

        text = await ask_groq(prompt, 250)

        if not text:
            raise Exception("No carousel")

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
                .strip()
                .upper()
            )

            if line:
                slides.append(line)

        return slides[:5]

    except Exception as e:

        print("CAROUSEL ERROR:", e)

        return [
            "AI МЕНЯЕТ ПРАВИЛА",
            "БУДУЩЕЕ УЖЕ ЗДЕСЬ",
            "НЕЙРОСЕТИ ПОБЕЖДАЮТ",
            "АВТОМАТИЗИРУЙ БЫСТРЕЕ",
            "НАЧНИ ПРЯМО СЕЙЧАС"
        ]


async def generate_content_plan():

    prompt = """
Создай контент-план на 7 дней.

Формат:

День 1:
Пост:
Карусель:
Reels:

И так до 7 дня.

Тематика:
AI
нейросети
автоматизация
заработок
AI бизнес

Стиль:
дорого
viral
современно
"""

    try:

        text = await ask_groq(prompt, 1000)

        if not text:
            return "Не удалось создать контент-план."

        return text[:4000]

    except Exception as e:

        print("PLAN ERROR:", e)

        return "Ошибка генерации контент-плана."


async def rewrite_text(text, style="viral"):

    style_prompt = REWRITE_STYLES.get(
        style,
        REWRITE_STYLES["viral"]
    )

    prompt = f"""
Перепиши текст.

Стиль:
{style_prompt}

Правила:
— короткие абзацы
— эмоционально
— удержание внимания
— современный стиль
— мощный hook
— без воды
— как дорогой AI creator

Текст:
{text}
"""

    try:

        result = await ask_groq(prompt, 1000)

        if not result:
            return "Не удалось переписать текст."

        return result[:4000]

    except Exception as e:

        print("REWRITE ERROR:", e)

        return "Ошибка rewrite."

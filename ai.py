import aiohttp
import random

from config import GROQ_API_KEY
from topics import TOPICS


HOOKS = [
    "95% людей используют AI неправильно",
    "Ты теряешь деньги без AI",
    "AI уже заменяет сотрудников",
    "Этот AI инструмент меняет всё",
    "Будущее уже наступило",
    "Контент больше никогда не будет прежним"
]


CTAS = [
    "Подпишись, чтобы не отстать от будущего.",
    "Сохрани пост и подпишись.",
    "Следи за AI трендами вместе с нами.",
    "Подписывайся на PrimeOnix AI.",
    "Начни использовать AI правильно уже сегодня."
]


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
        "temperature": 1.1,
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

    hook = random.choice(HOOKS)
    cta = random.choice(CTAS)

    prompt = f"""
Напиши вирусный Telegram пост на русском.

Тема: {topic}
Категория: {category}

Стиль:
— короткие абзацы
— без воды
— современно
— как AI creator
— легко читается
— цепляющий тон

Структура:
1. Hook
2. Проблема
3. Почему это важно
4. AI решение
5. CTA

Начни с:
{hook}

В конце:
{cta}
"""

    try:
        text = await ask_groq(prompt, 700)

        if not text:
            return "🚀 AI меняет рынок прямо сейчас.", topic

        return text[:3500], topic

    except Exception as e:
        print("AI ERROR:", e)
        return "🚀 AI меняет рынок прямо сейчас.", topic


async def generate_carousel(topic):
    prompt = f"""
Создай 5 коротких слайдов для Instagram AI carousel.

Тема:
{topic}

Формат:
1. HOOK
2. ПРОБЛЕМА
3. ВАЖНОСТЬ
4. AI РЕШЕНИЕ
5. CTA

Правила:
— каждый слайд максимум 6 слов
— текст должен быть мощным
— без пояснений
— только строки с текстом
— на русском
"""

    try:
        text = await ask_groq(prompt, 300)

        if not text:
            raise Exception("No carousel text")

        slides = []

        for line in text.split("\n"):
            line = line.strip()

            if not line:
                continue

            for item in [
                "1.", "2.", "3.", "4.", "5.",
                "HOOK", "ПРОБЛЕМА", "ВАЖНОСТЬ",
                "AI РЕШЕНИЕ", "CTA", ":"
            ]:
                line = line.replace(item, "")

            line = line.strip()

            if line:
                slides.append(line)

        return slides[:5]

    except Exception as e:
        print("CAROUSEL AI ERROR:", e)

        return [
            "AI меняет рынок",
            "Ты теряешь время",
            "Конкуренты уже впереди",
            "Автоматизируй контент",
            "Начни прямо сейчас"
        ]

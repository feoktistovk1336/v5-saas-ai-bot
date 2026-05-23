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
    "Большинство не понимают силу AI",
    "Через 1 год будет поздно",
    "Контент больше никогда не будет прежним"
]


CTAS = [
    "Подпишись, чтобы не отстать от будущего.",
    "Сохрани пост и подпишись.",
    "Следи за AI трендами вместе с нами.",
    "Подписывайся на V5 AI SaaS.",
    "Подпишись и начни использовать AI правильно."
]


async def generate_text():

    category = random.choice(list(TOPICS.keys()))
    topic = random.choice(TOPICS[category])
    hook = random.choice(HOOKS)
    cta = random.choice(CTAS)

    prompt = f"""
Напиши мощный вирусный Telegram пост.

Тема: {topic}
Категория: {category}

Стиль:
— короткие абзацы
— viral Instagram / TikTok style
— без воды
— современно
— как AI creator

Структура:
1. Hook
2. Проблема
3. Почему это важно
4. AI решение
5. CTA

Начни с:
{hook}

В конце добавь CTA:
{cta}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1.2,
        "max_tokens": 700
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=json_data
            ) as response:

                data = await response.json()

                if "choices" not in data:
                    print("AI RESPONSE ERROR:", data)
                    return "🚀 AI сейчас перегружен. Попробуй позже.", topic

                text = data["choices"][0]["message"]["content"]
                return text[:3500], topic

    except Exception as e:
        print("AI ERROR:", e)
        return "🚀 AI меняет рынок прямо сейчас.", topic


async def generate_carousel(topic):

    prompt = f"""
Создай Instagram AI carousel на русском.

Тема:
{topic}

Нужно 5 коротких слайдов.

Формат:
1. HOOK
2. ПРОБЛЕМА
3. ПОЧЕМУ ЭТО ВАЖНО
4. AI РЕШЕНИЕ
5. CTA

Каждый слайд максимум 8 слов.
Только текст слайдов.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1,
        "max_tokens": 300
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=json_data
            ) as response:

                data = await response.json()

                if "choices" not in data:
                    print("CAROUSEL AI ERROR:", data)
                    raise Exception("No choices")

                text = data["choices"][0]["message"]["content"]

                slides = [
                    line.strip()
                    for line in text.split("\n")
                    if line.strip()
                ]

                return slides[:5]

    except Exception as e:
        print("CAROUSEL AI ERROR:", e)

        return [
            "AI меняет рынок",
            "Ты теряешь время",
            "Конкуренты уже используют AI",
            "Автоматизируй контент",
            "Подпишись сейчас"
        ]

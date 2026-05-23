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
Напиши мощный Telegram-пост на русском.

Тема:
{topic}

Главная идея для картинки:
{visual_title}

Стиль:
— дерзко
— короткие абзацы
— без воды
— как AI creator / SaaS founder
— продающе
— удерживает внимание
— современный Telegram стиль

Структура:
1. Сильный хук
2. Боль аудитории
3. Почему старый подход больше не работает
4. Как AI решает проблему
5. Мотивационный CTA подписаться

Не используй длинные абзацы.
Не пиши скучно.
Не используй фразу "в современном мире".
"""

    try:
        text = await ask_groq(prompt, 800)

        if not text:
            return "AI меняет рынок. Кто действует сейчас — получает преимущество.", visual_title

        return text[:3500], visual_title

    except Exception as e:
        print("AI ERROR:", e)
        return "AI меняет рынок. Кто действует сейчас — получает преимущество.", visual_title


async def generate_carousel(topic):
    prompt = f"""
Создай 5 слайдов для дорогой AI/SaaS Instagram-карусели.

Тема:
{topic}

Формат:
Только 5 строк.
Каждая строка — отдельный слайд.

Стиль текста:
— коротко
— мощно
— продающе
— максимум 5 слов
— как заголовок на рекламном креативе
— без нумерации
— без пояснений

Примеры:
AI ОТКРЫВАЕТ ВОЗМОЖНОСТИ
СТАРЫЕ МЕТОДЫ УМИРАЮТ
АВТОМАТИЗИРУЙ СЕЙЧАС
БУДУЩЕЕ ЗА БЫСТРЫМИ
НАЧНИ ПРЯМО СЕГОДНЯ
"""

    try:
        text = await ask_groq(prompt, 250)

        if not text:
            raise Exception("No carousel text")

        slides = []

        for line in text.split("\n"):
            line = line.strip()

            if not line:
                continue

            line = (
                line.replace("1.", "")
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

    except Exception as e:
        print("CAROUSEL AI ERROR:", e)

        return [
            "AI МЕНЯЕТ ПРАВИЛА",
            "СТАРЫЕ МЕТОДЫ УМИРАЮТ",
            "АВТОМАТИЗИРУЙ СЕЙЧАС",
            "ВЫИГРЫВАЙ ВРЕМЯ",
            "НАЧНИ ПРЯМО СЕГОДНЯ"
        ]


async def generate_content_plan():
    prompt = """
Составь контент-план на 7 дней для Telegram-канала про AI, нейросети, бизнес и автоматизацию.

Формат строго:

День 1:
Пост:
Карусель:
Reels:

День 2:
Пост:
Карусель:
Reels:

И так до 7 дня.

Стиль:
— продающий
— современный
— для AI/SaaS проекта
— темы должны быть разные
— без воды
— коротко
"""

    try:
        text = await ask_groq(prompt, 1000)

        if not text:
            return "📅 Не удалось создать контент-план. Попробуй позже."

        return text[:4000]

    except Exception as e:
        print("CONTENT PLAN ERROR:", e)
        return "📅 Не удалось создать контент-план. Попробуй позже."

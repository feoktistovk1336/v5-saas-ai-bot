import aiohttp
import random

from config import GROQ_API_KEY
from topics import TOPICS


# ================= HOOKS =================
HOOKS = [

    "95% людей используют AI неправильно",
    "Ты теряешь деньги без AI",
    "AI уже заменяет сотрудников",
    "Этот AI инструмент меняет всё",
    "Будущее уже наступило",
    "Большинство не понимают силу AI",
    "Через 1 год будет поздно",
    "AI делает это вместо команды из 10 человек",
    "Ты сильно недооцениваешь AI",
    "Контент больше никогда не будет прежним"

]


# ================= CTA =================
CTAS = [

    "Подпишись, чтобы не отстать от будущего.",
    "Сохрани пост и подпишись.",
    "Следи за AI трендами вместе с нами.",
    "Подписывайся на V5 AI SaaS.",
    "Завтра этим будут пользоваться все.",
    "Подпишись и начни использовать AI правильно."

]


# ================= GENERATE TEXT =================
async def generate_text():

    # категория
    category = random.choice(
        list(TOPICS.keys())
    )

    # тема
    topic = random.choice(
        TOPICS[category]
    )

    # hook
    hook = random.choice(HOOKS)

    # cta
    cta = random.choice(CTAS)

    prompt = f"""
Напиши мощный вирусный Telegram пост.

Тема:
{topic}

Категория:
{category}

Стиль:
— modern AI creator
— viral Instagram style
— TikTok style
— короткие абзацы
— сильные эмоции
— ощущение будущего
— без воды
— легко читать

Структура:

1. Сильный HOOK
2. Боль / проблема
3. Почему это важно
4. AI решение
5. CTA

Правила:
— НЕ пиши длинные абзацы
— НЕ используй сложные слова
— Делай текст как viral creator
— Добавляй энергию
— Делай стиль как startup founder

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

                print(data)

                if "choices" not in data:

                    return (
                        "🚀 AI сейчас перегружен. Попробуй позже.",
                        topic
                    )

                text = data["choices"][0]["message"]["content"]

                # защита от слишком длинного текста
                text = text[:3500]

                return text, topic

    except Exception as e:

        print("AI ERROR:", e)

        return (
            "🚀 AI меняет рынок прямо сейчас.",
            topic
        )

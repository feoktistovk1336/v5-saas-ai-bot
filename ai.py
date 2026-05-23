import aiohttp
import random

from config import GROQ_API_KEY


TOPICS = [

    "AI бизнес",
    "нейросети",
    "автоматизация",
    "ChatGPT",
    "заработок на AI",
    "AI инструменты",
    "будущее AI",
    "AI маркетинг",
    "AI стартапы",
    "AI контент"

]


HOOKS = [

    "95% людей используют AI неправильно",
    "Ты теряешь деньги без AI",
    "AI уже заменяет сотрудников",
    "Этот AI инструмент меняет всё",
    "Будущее уже наступило",
    "Большинство не понимают силу AI"

]


# ================= GENERATE TEXT =================
async def generate_text():

    topic = random.choice(TOPICS)

    hook = random.choice(HOOKS)

    prompt = f"""
Напиши короткий вирусный пост для Telegram.

Тема:
{topic}

Структура:

1. Мощный hook
2. Проблема
3. Решение
4. AI инструмент
5. Призыв подписаться

Стиль:
— современно
— viral style
— короткие абзацы
— как AI creator блог

Начни с:
{hook}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1
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

                return text, topic

    except Exception as e:

        print("AI ERROR:", e)

        return (
            "🚀 AI меняет рынок прямо сейчас.",
            topic
        )

import aiohttp
from config import GROQ_API_KEY
import random

TOPICS = [
    "AI trends 2026",
    "Future of content creation",
    "AI tools that change everything",
    "Viral marketing secrets",
]

async def generate_text():
    topic = random.choice(TOPICS)

    prompt = f"""
    Ты viral AI creator.

    Тема: {topic}

    Дай:
    - сильный hook
    - короткие абзацы
    - emoji
    - CTA
    """

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9
            }
        ) as r:
            data = await r.json()
            return data["choices"][0]["message"]["content"], topic

async def generate_content_factory():

    prompt = """
Создай мощный AI Content Factory Pack.

Нужно:

1. 10 VIRAL HOOKS
2. 10 AI POST IDEAS
3. 10 REELS IDEAS
4. 10 CAROUSEL IDEAS
5. 10 POWERFUL CTA

Тематика:
AI
нейросети
автоматизация
AI бизнес
AI маркетинг
заработок через AI

Стиль:
— современно
— дорого
— viral
— коротко
— эмоционально
— aggressive marketing
— creator economy style

Формат:
используй заголовки разделов.
"""

    try:

        text = await ask_groq(
            prompt,
            1800
        )

        if not text:
            return "Не удалось создать контент."

        return text[:12000]

    except Exception as e:

        print("FACTORY ERROR:", e)

        return "Ошибка генерации контент-завода."

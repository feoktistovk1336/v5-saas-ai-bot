import aiohttp
import random

# IMAGE GENERATION
async def generate_images(prompt: str, count=5):
    images = []

    for i in range(count):
        url = f"https://image.pollinations.ai/prompt/{prompt}, cinematic {i}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    images.append(await r.read())

    return images


# MOCK REELS (пока без ffmpeg)
async def generate_reels_text(topic: str):
    return f"""
🔥 VIRAL REELS SCRIPT

Hook: You are not ready for this AI shift...

Topic: {topic}

CTA: follow for more AI content 🚀
"""

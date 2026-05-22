import aiohttp


# ================= IMAGE GENERATION =================
async def generate_images(prompt: str, count=5):
    images = []

    async with aiohttp.ClientSession() as session:

        for i in range(count):

            url = (
                f"https://image.pollinations.ai/prompt/"
                f"{prompt}%20cinematic%20{i}"
            )

            try:
                async with session.get(url) as r:

                    if r.status == 200:
                        # сохраняем URL, а не bytes
                        images.append(url)

                    else:
                        print("IMAGE STATUS:", r.status)

            except Exception as e:
                print("IMAGE ERROR:", e)

    return images


# ================= MOCK REELS =================
async def generate_reels_text(topic: str):

    return f"""
🔥 VIRAL REELS SCRIPT

Hook: You are not ready for this AI shift...

Topic: {topic}

CTA: follow for more AI content 🚀
"""

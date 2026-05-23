# ================= GENERATE IMAGES =================
async def generate_images(topic, count=5):

    images = []

    styles = [

        "cinematic lighting",
        "ultra realistic",
        "cyberpunk",
        "futuristic AI",
        "neon glow",
        "instagram viral style",
        "dark luxury",
        "modern startup",
        "3d render",
        "digital future"

    ]

    for _ in range(count):

        style = random.choice(styles)

        seed = random.randint(
            1,
            99999999
        )

        prompt = (
            f"{topic}, "
            f"{style}, "
            f"AI business, "
            f"viral instagram post, "
            f"high quality, "
            f"ultra detailed, "
            f"4k"
        )

        url = (
            "https://image.pollinations.ai/prompt/"
            f"{prompt}?seed={seed}&width=1080&height=1080"
        )

        images.append(url)

    return images

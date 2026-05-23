import os
import random
import aiohttp
import replicate

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from config import REPLICATE_API_TOKEN, BRAND_USERNAME


AI_FALLBACKS = [
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&q=95",
    "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1080&q=95",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=1080&q=95"
]


def load_font(size):
    paths = [
        "Montserrat-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]

    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass

    return ImageFont.load_default()


def clean_text(text):
    for item in ["🔥", "🚀", "✅", "❌", "💡", "1.", "2.", "3.", "4.", "5.", ":"]:
        text = text.replace(item, "")

    return text.strip().upper()


def wrap_lines(text, max_chars):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = f"{line} {word}".strip()

        if len(test) <= max_chars:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines


def fit_title(draw, text, max_width, max_height):
    clean = clean_text(text)

    for size in range(86, 38, -4):
        font = load_font(size)
        max_chars = max(8, int(max_width / (size * 0.58)))
        lines = wrap_lines(clean, max_chars)

        line_height = int(size * 1.08)
        total_height = len(lines) * line_height

        widest = 0

        for line in lines:
            box = draw.textbbox((0, 0), line, font=font)
            widest = max(widest, box[2] - box[0])

        if widest <= max_width and total_height <= max_height:
            return font, lines[:4], line_height

    font = load_font(42)
    return font, wrap_lines(clean, 13)[:4], 48


async def generate_ai_background(topic):
    if not REPLICATE_API_TOKEN:
        return random.choice(AI_FALLBACKS)

    try:
        client = replicate.Client(api_token=REPLICATE_API_TOKEN)

        prompt = f"""
premium cinematic AI SaaS poster,
{topic},
dark futuristic city,
orange glow,
luxury marketing creative,
high contrast,
ultra detailed,
modern tech branding,
viral instagram visual
"""

        output = client.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "go_fast": True,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "output_quality": 95
            }
        )

        if output and len(output) > 0:
            return str(output[0])

    except Exception as e:
        print("REPLICATE ERROR:", e)

    return random.choice(AI_FALLBACKS)


async def create_poster(image_url, title, show_brand=True):
    try:
        os.makedirs("generated", exist_ok=True)

        temp_file = f"generated/temp_{random.randint(1, 999999)}.jpg"
        final_file = f"generated/final_{random.randint(1, 999999)}.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    return None

                with open(temp_file, "wb") as f:
                    f.write(await response.read())

        image = Image.open(temp_file).convert("RGBA")
        image = image.resize((1080, 1080))

        dark = Image.new("RGBA", image.size, (0, 0, 0, 95))
        image = Image.alpha_composite(image, dark)

        glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)

        for r in range(520, 0, -10):
            alpha = int(90 * (r / 520))
            gd.ellipse(
                [(760 - r, 680 - r), (760 + r, 680 + r)],
                fill=(255, 170, 30, alpha)
            )

        image = Image.alpha_composite(image, glow)

        draw = ImageDraw.Draw(image)

        card_x = 70
        card_y = 145
        card_w = 780
        card_h = 810

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)

        sd.rounded_rectangle(
            [(card_x + 20, card_y + 22), (card_x + card_w + 20, card_y + card_h + 22)],
            radius=60,
            fill=(0, 0, 0, 140)
        )

        shadow = shadow.filter(ImageFilter.GaussianBlur(20))
        image = Image.alpha_composite(image, shadow)

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(card_x, card_y), (card_x + card_w, card_y + card_h)],
            radius=60,
            fill=(3, 8, 18, 226),
            outline=(255, 255, 255, 80),
            width=2
        )

        font_badge = load_font(24)
        font_sub = load_font(34)
        font_brand = load_font(25)

        draw.rounded_rectangle(
            [(card_x + 55, card_y + 55), (card_x + 275, card_y + 108)],
            radius=26,
            fill=(255, 255, 255, 22),
            outline=(255, 255, 255, 80),
            width=1
        )

        draw.text((card_x + 83, card_y + 69), "AI CREATIVE +", fill=(235, 235, 235), font=font_badge)

        title_font, lines, line_height = fit_title(draw, title, card_w - 120, 410)

        text_y = card_y + 170

        for i, line in enumerate(lines):
            color = (255, 218, 35) if i in [1, 2] else (255, 255, 255)
            draw.text((card_x + 55, text_y), line, fill=color, font=title_font)
            text_y += line_height

        subtitle_y = card_y + 545

        draw.text((card_x + 55, subtitle_y), "ТЕХНОЛОГИИ МЕНЯЮТ МИР.", fill=(235, 235, 235), font=font_sub)
        draw.text((card_x + 55, subtitle_y + 48), "ВОПРОС ТОЛЬКО В ТОМ,", fill=(235, 235, 235), font=font_sub)
        draw.text((card_x + 55, subtitle_y + 96), "ИСПОЛЬЗУЕШЬ ЛИ ТЫ ИХ.", fill=(255, 218, 35), font=font_sub)

        draw.rectangle(
            [(card_x + 55, card_y + card_h - 158), (card_x + 175, card_y + card_h - 149)],
            fill=(255, 210, 35)
        )

        draw.text((card_x + 55, card_y + card_h - 110), "AI CONTENT", fill=(255, 255, 255), font=font_sub)

        if show_brand:
            badge_x = card_x + 55
            badge_y = card_y + card_h - 62

            draw.rounded_rectangle(
                [(badge_x, badge_y), (badge_x + 330, badge_y + 46)],
                radius=23,
                fill=(0, 0, 0, 65),
                outline=(255, 218, 35, 180),
                width=2
            )

            draw.text((badge_x + 28, badge_y + 9), BRAND_USERNAME, fill=(255, 255, 255), font=font_brand)

        image.convert("RGB").save(final_file, quality=97)

        try:
            os.remove(temp_file)
        except Exception:
            pass

        return final_file

    except Exception as e:
        print("CREATE POSTER ERROR:", e)
        return None

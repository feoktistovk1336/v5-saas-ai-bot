import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # например "-100123"
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
STRIPE_KEY = os.getenv("STRIPE_KEY")

DB_PATH = "data.db"

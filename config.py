import os

from dotenv import load_dotenv

load_dotenv()


# ================= BOT =================
BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

ADMIN_ID = int(
    os.getenv("ADMIN_ID")
)

CHANNEL_ID = int(
    os.getenv("CHANNEL_ID")
)


# ================= AI =================
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# ================= DATABASE =================
DB_PATH = "database.db"

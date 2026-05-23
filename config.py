import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

BRAND_USERNAME = "@primeonix26"

FREE_LIMIT = 5
PRO_PRICE_STARS = 199
PRO_DAYS = 30
DB_PATH = "database.sqlite"

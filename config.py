import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

BOT_USERNAME = os.getenv("BOT_USERNAME", "primeonixbot")

BRAND_USERNAME = "@primeonix26"

DB_PATH = "database.db"

FREE_LIMIT = 5
PRO_PRICE_STARS = 199
PRO_DAYS = 30

REPLICATE_API_TOKEN = "r8_9ytQuNda8ki6mfmz066ikudBezV2L3a37xiBe"

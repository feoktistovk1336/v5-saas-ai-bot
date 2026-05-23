import time
import aiosqlite

from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            plan TEXT DEFAULT 'FREE',
            generations INTEGER DEFAULT 0,
            pro_until INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            content TEXT,
            created_at INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            currency TEXT,
            charge_id TEXT,
            created_at INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        await db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("autopost_enabled", "1")
        )

        await db.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            ("autopost_hours", "3")
        )

        await db.commit()


async def create_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        await db.commit()


async def get_user(user_id):
    await create_user(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, plan, generations, pro_until FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()


async def is_pro(user_id):
    user = await get_user(user_id)

    if not user:
        return False

    return user[1] == "PRO" and (user[3] or 0) > int(time.time())


async def set_pro(user_id, days):
    await create_user(user_id)

    pro_until = int(time.time()) + days * 24 * 60 * 60

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET plan = 'PRO', pro_until = ? WHERE user_id = ?",
            (pro_until, user_id)
        )
        await db.commit()


async def can_generate(user_id, free_limit):
    user = await get_user(user_id)

    if await is_pro(user_id):
        return True

    return (user[2] or 0) < free_limit


async def add_generation(user_id, gen_type, content):
    await create_user(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO generations (user_id, type, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, gen_type, content, int(time.time()))
        )

        await db.execute(
            "UPDATE users SET generations = generations + 1 WHERE user_id = ?",
            (user_id,)
        )

        await db.commit()


async def add_payment(user_id, amount, currency, charge_id):
    await create_user(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO payments (user_id, amount, currency, charge_id, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, currency, charge_id, int(time.time()))
        )
        await db.commit()


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        users = await cursor.fetchone()

        cursor = await db.execute("SELECT COUNT(*) FROM generations")
        gens = await cursor.fetchone()

        cursor = await db.execute("SELECT COUNT(*) FROM payments")
        pays = await cursor.fetchone()

        return users[0], gens[0], pays[0]


async def get_setting(key, default=None):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT value FROM settings WHERE key = ?",
            (key,)
        )
        row = await cursor.fetchone()

        return row[0] if row else default


async def set_setting(key, value):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, str(value))
        )
        await db.commit()

import aiosqlite

from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            plan TEXT DEFAULT 'FREE',
            generations INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            content TEXT
        )
        """)

        await db.commit()


async def create_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,)
        )

        await db.commit()


async def add_generation(user_id, gen_type, content):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO generations (user_id, type, content)
            VALUES (?, ?, ?)
            """,
            (user_id, gen_type, content)
        )

        await db.execute(
            """
            UPDATE users
            SET generations = generations + 1
            WHERE user_id = ?
            """,
            (user_id,)
        )

        await db.commit()


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        users = await cursor.fetchone()

        cursor = await db.execute("SELECT COUNT(*) FROM generations")
        gens = await cursor.fetchone()

        return users[0], gens[0]

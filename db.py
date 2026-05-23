import sqlite3
import aiosqlite


DB_PATH = "database.db"


# ================= INIT =================
async def init_db():

    async with aiosqlite.connect(DB_PATH) as db:

        # users
        await db.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            plan TEXT DEFAULT 'FREE',
            generations INTEGER DEFAULT 0

        )

        """)

        # generations history
        await db.execute("""

        CREATE TABLE IF NOT EXISTS generations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            content TEXT

        )

        """)

        await db.commit()


# ================= CREATE USER =================
async def create_user(user_id):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """

            INSERT OR IGNORE INTO users (
                user_id
            )

            VALUES (?)

            """,
            (user_id,)
        )

        await db.commit()


# ================= GET USER =================
async def get_user(user_id):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """

            SELECT *
            FROM users
            WHERE user_id = ?

            """,
            (user_id,)
        )

        return await cursor.fetchone()


# ================= ADD GENERATION =================
async def add_generation(
    user_id,
    gen_type,
    content
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """

            INSERT INTO generations (
                user_id,
                type,
                content
            )

            VALUES (?, ?, ?)

            """,
            (
                user_id,
                gen_type,
                content
            )
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


# ================= GET STATS =================
async def get_stats():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """

            SELECT COUNT(*)
            FROM users

            """
        )

        users = await cursor.fetchone()

        cursor2 = await db.execute(
            """

            SELECT COUNT(*)
            FROM generations

            """
        )

        gens = await cursor2.fetchone()

        return users[0], gens[0]

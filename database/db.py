import aiosqlite


DB_NAME = "database.sqlite"


async def init_db():

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE
        )
        """)

        await db.commit()


async def create_user(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (telegram_id)
            VALUES (?)
            """,
            (user_id,)
        )

        await db.commit()

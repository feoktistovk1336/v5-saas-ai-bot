from fastapi import FastAPI
import aiosqlite

app = FastAPI()


@app.get("/admin/users")
async def users():
    async with aiosqlite.connect("data.db") as db:
        cur = await db.execute("SELECT * FROM users")
        return await cur.fetchall()


@app.get("/admin/stats")
async def stats():
    async with aiosqlite.connect("data.db") as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        users = await cur.fetchone()
        return {"users": users[0]}

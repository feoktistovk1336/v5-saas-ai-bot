import asyncio
from typing import Awaitable, Callable

generation_queue = asyncio.Queue()


async def add_to_queue(user_id: int, task_name: str, coro_func: Callable[[], Awaitable]):
    await generation_queue.put({
        "user_id": user_id,
        "task_name": task_name,
        "coro_func": coro_func
    })


async def queue_worker():
    while True:
        job = await generation_queue.get()

        try:
            await job["coro_func"]()
        except Exception as e:
            print(f"QUEUE ERROR: {e}")
        finally:
            generation_queue.task_done()

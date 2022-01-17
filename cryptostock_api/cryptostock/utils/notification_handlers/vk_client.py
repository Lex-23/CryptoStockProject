import asyncio
import os
from functools import wraps

from vkbottle import API

api = API(os.getenv("VK_BOT_API_TOKEN"))


def asyncio_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.run(func(*args, **kwargs))

    return wrapper


@asyncio_run
async def vk_notify(message: str, context: dict):
    await api.messages.send(message=message, peer_id=context["peer_id"], random_id=0)

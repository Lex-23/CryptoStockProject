import asyncio
import os
import random
import re
from functools import wraps

from vkbottle import API

api = API(os.getenv("VK_BOT_API_TOKEN"))


def asyncio_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))

    return wrapper


@asyncio_run
async def vk_notify(message: str, context: dict):
    edit_message = "".join(re.split(r"<\w+>|</\w+>", message))
    await api.messages.send(
        message=edit_message,
        peer_id=context["peer_id"],
        random_id=random.randint(-2147483648, +2147483648),
    )

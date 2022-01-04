import os
from functools import wraps

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN"))
dispatcher = Dispatcher(bot, storage=RedisStorage2())


def executor_start(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        executor.start(dispatcher, func(*args, **kwargs))

    return wrapper


@executor_start
async def tg_notify(message, **kwargs):
    tg_chat_id = kwargs["tg_chat_id"]
    await bot.send_message(tg_chat_id, message)

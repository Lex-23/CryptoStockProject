import os
from functools import wraps

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

TELEGRAM_STORAGE_HOST = os.environ["TELEGRAM_STORAGE_HOST"]
TELEGRAM_STORAGE_PORT = os.environ["TELEGRAM_STORAGE_PORT"]

bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN"))
dispatcher = Dispatcher(
    bot,
    storage=RedisStorage2(host=TELEGRAM_STORAGE_HOST, port=int(TELEGRAM_STORAGE_PORT)),
)


def executor_start(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        executor.start(dispatcher, func(*args, **kwargs))

    return wrapper


@executor_start
async def tg_notify(message, context):
    # TODO: validate context
    await bot.send_message(context["chat_id"], message, parse_mode="html")

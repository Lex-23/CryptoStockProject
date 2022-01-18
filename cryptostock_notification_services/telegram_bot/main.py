import logging
import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

storage = RedisStorage2()

bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN"))
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    start_buttons = ["get chat id", "notify: TURN ON"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.reply(
        "Click *get chat id* for apply notifications for telegram.",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi!\nI'm CryptostockBot!\nPowered by aiogram.\n"
        "For more information input *\\start*.",
        parse_mode="Markdown",
    )


@dp.message_handler(Text(equals="get chat id"))
async def get_chat_id(message: types.Message):
    chat_id = message.from_user.id
    await message.reply(
        f"Your personal chat id: *{chat_id}*\n"
        f"Please input this id to application service,\n"
        f"if you want getting notifications in telegram.",
        parse_mode="Markdown",
    )
    logging.info(f"chat_id: {chat_id}")
    return chat_id


@dp.message_handler(Text(equals="notify: TURN ON"))
async def notify_on(message: types.Message):
    await message.reply("Notification to tg is ON")
    chat_id = message.from_user.id
    payload = {"id": chat_id}
    requests.get("http://127.0.0.1:8000/notify-on", params=payload)
    logging.info("notification TURN ON")

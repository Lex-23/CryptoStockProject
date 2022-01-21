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

TELEGRAM_BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]
TELEGRAM_NOTIFICATION_ACTIVATE_URL = os.environ["TELEGRAM_NOTIFICATION_ACTIVATE_URL"]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    start_buttons = ["get chat id"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    arguments = message.get_args()

    if arguments:
        chat_id = message.from_user.id
        payload = {
            "source": TELEGRAM_BOT_NAME,
            "account_token": arguments,
            "chat_id": chat_id,
        }

        response = requests.post(TELEGRAM_NOTIFICATION_ACTIVATE_URL, data=payload)
        logging.info("notification TURN ON in process")
        await message.reply(
            "*Activating notifications in process*. Please wait success message",
            reply_markup=keyboard,
            parse_mode="Markdown",
        )

        if response.status_code != 200:
            await message.reply(
                "*Activating notifications failure*. Please, try again or write to support.",
                reply_markup=keyboard,
                parse_mode="Markdown",
            )

    else:
        await message.reply(
            "Welcome!\nClick *get chat id* for apply notifications for telegram, if you need.",
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

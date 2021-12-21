import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

storage = RedisStorage2()

bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN"))
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    start_buttons = ["get chat id"]
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
    user_chat_id = message.from_user.id
    await message.reply(
        f"Your personal chat id: *{user_chat_id}*\n"
        f"Please input this id to application service,\n"
        f"if you want getting notifications in telegram.",
        parse_mode="Markdown",
    )
    logging.info(f"user_chat_id: {user_chat_id}")
    return user_chat_id


async def notification(chat_id, text):
    logging.info(f"Sent msg {text} \nto user with chat_id {chat_id}")
    await bot.send_message(chat_id, text)


if 2 == 2:
    executor.start(dp, notification(chat_id=5073863383, text="Hello bro"))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

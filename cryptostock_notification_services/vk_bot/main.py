import os

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message

bot = Bot(token=os.getenv("VK_BOT_API_TOKEN"))


@bot.on.message(text="Hello")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Hello, {}".format(users_info[0].first_name))


@bot.on.message(text=["help", "info"])
async def help_handler(message: Message):
    await message.answer(
        "Hi!\nI'm CryptostockBot!\nPowered by vkbottle.\n"
        "Please, click 'start' or 'menu'"
    )


@bot.on.private_message(text=["menu", "start", "/start", "enter"])
@bot.on.private_message(payload={"cmd": "menu"})
async def menu(message: Message):
    await message.answer(
        message="Click 'get id' for getting your peer id",
        keyboard=(
            Keyboard(one_time=False, inline=False).add(
                Text("get id"), color=KeyboardButtonColor.POSITIVE
            )
        ),
    )


@bot.on.private_message(text="get id")
async def get_id(message: Message):
    await message.answer(
        f"Please input this id to your own account in stock application:"
        f"\n{message.peer_id}"
    )

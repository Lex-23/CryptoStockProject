import os

from vkbottle.bot import Bot, Message

bot = Bot(token=os.getenv("VK_BOT_API_TOKEN"))


@bot.on.message(text="<msg>")
async def echo_answer(ans: Message, msg):
    await ans.answer("Ты написал: %s" % (msg))


@bot.on.message(text="Hello")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Hello, {}".format(users_info[0].first_name))

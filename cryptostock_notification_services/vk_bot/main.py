import json
import os

import requests
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message

VK_NOTIFICATION_ACTIVATE_URL = os.environ["VK_NOTIFICATION_ACTIVATE_URL"]
VK_BOT_PUBLIC_NUMBER = os.environ["VK_BOT_PUBLIC_NUMBER"]
bot = Bot(token=os.getenv("VK_BOT_API_TOKEN"))
bot.labeler.vbml_ignore_case = True


@bot.on.private_message(
    text=["menu", "info", "help", "start", "/start", "enter", "начать"]
)
@bot.on.private_message(payload={"cmd": "menu"})
async def menu(message: Message):
    arguments = message.ref
    if arguments:
        await message.answer(
            message="Please, click 'activate notifications' for activating notifications.",
            keyboard=(
                Keyboard(one_time=True, inline=False).add(
                    Text(
                        "activate notifications",
                        payload={
                            "source": VK_BOT_PUBLIC_NUMBER,
                            "account_token": message.ref,
                            "peer_id": message.peer_id,
                        },
                    ),
                    color=KeyboardButtonColor.POSITIVE,
                )
            ).get_json(),
        )
    else:
        await message.answer(
            message="Please, click 'get id' for getting chat_id.",
            keyboard=(
                Keyboard(one_time=True, inline=False).add(
                    Text("get id"), color=KeyboardButtonColor.POSITIVE
                )
            ).get_json(),
        )


@bot.on.private_message(text="get id")
async def get_id(message: Message):
    await message.answer(
        f"Please input this id to your own account in stock application:"
        f"\n{message.peer_id}"
    )


@bot.on.private_message(text="activate notifications")
async def activate(message: Message):
    response = requests.post(
        VK_NOTIFICATION_ACTIVATE_URL, data=json.loads(message.payload)
    )
    if response.status_code != 200:
        await message.answer(
            "Activating notifications failure. Please, try again or write to support."
        )

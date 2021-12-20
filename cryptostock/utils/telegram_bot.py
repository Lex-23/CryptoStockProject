from secrets import token_urlsafe

import telepot

user_token = token_urlsafe(8)
# print(user_token)


token = "5081655043:AAF38F7RTTkJKMx_LGZNim2LqR_QvFJoQQM"
receiver_id = 5073863383
receiver_id_1 = 462188519

bot = telepot.Bot(token)
info = bot.getChat(462188519)
response = bot.getUpdates()

print(response)
breakpoint()
bot.sendMessage(receiver_id, "user_token")

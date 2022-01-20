import os

from account.models import Account
from notification.models import Consumer, ConsumerType
from utils.api_view_assistants import generate_new_account_token

TELEGRAM_BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]


def create_telegram_join_url(account):
    generate_new_account_token(account)
    return {
        "join_url": f"https://t.me/{TELEGRAM_BOT_NAME}?start={account.account_token}"
    }


CONSUMER_ACTIVATE_DATA = {
    "TELEGRAM": create_telegram_join_url,
    "VK": None,  # TODO
    "EMAIL": None,  # TODO
}


def join_tg_consumer_with_bot(account_token, tg_chat_id):
    account = Account.objects.get(account_token=account_token)
    consumer = Consumer.objects.get(account=account, type=ConsumerType.TELEGRAM)
    consumer.data["tg_chat_id"] = tg_chat_id
    consumer.save()
    account.reset_account_token()
    account.save()

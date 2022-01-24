import os

from django.db import transaction
from notification.models import Consumer, ConsumerType
from utils.api_view_assistants import generate_new_account_token
from utils.validators import validate_recipient_exists

TELEGRAM_BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]


def create_telegram_join_url(account):
    generate_new_account_token(account)
    return {
        "join_url": f"https://t.me/{TELEGRAM_BOT_NAME}?start={account.account_token}"
    }


def add_recipient(account, **kwargs):
    recipient = kwargs["recipient"]
    consumer = Consumer.objects.get(account=account, type=ConsumerType.EMAIL)
    if not consumer.data.get("recipient"):
        consumer.data["recipient"] = [recipient]
    else:
        validate_recipient_exists(consumer, recipient)
        consumer.data["recipient"].append(recipient)
    consumer.save()
    return recipient


CONSUMER_ACTIVATE_DATA = {
    "TELEGRAM": create_telegram_join_url,
    "VK": None,  # TODO
    "EMAIL": add_recipient,
}


@transaction.atomic
def join_tg_consumer_with_bot(account, tg_chat_id):
    consumer = Consumer.objects.get(account=account, type=ConsumerType.TELEGRAM)
    consumer.data["tg_chat_id"] = tg_chat_id
    account.reset_account_token()
    consumer.save()
    account.save()

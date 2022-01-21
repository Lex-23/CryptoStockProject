import os

from account.models import Account
from celery_tasks.general_notification_tasks import success_tg_notification_activate
from notification.models import Consumer, ConsumerType
from utils.api_view_assistants import generate_new_account_token
from utils.validators import validate_recipient, validate_recipient_exists

TELEGRAM_BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]


def create_telegram_join_url(account):
    generate_new_account_token(account)
    return {
        "join_url": f"https://t.me/{TELEGRAM_BOT_NAME}?start={account.account_token}"
    }


def add_recipient(account, **kwargs):
    breakpoint()
    recipient = kwargs["recipient"]
    breakpoint()
    for item in recipient:
        validate_recipient(item)
    consumer = Consumer.objects.get(account=account, type=ConsumerType.EMAIL)
    if not consumer.data.get("recipient"):
        consumer.data["recipient"] = [recipient]
    else:
        validate_recipient_exists(consumer, recipient)
        consumer.data["recipient"].append(recipient)
    return recipient


CONSUMER_ACTIVATE_DATA = {
    "TELEGRAM": create_telegram_join_url,
    "VK": None,  # TODO
    "EMAIL": add_recipient,
}


def join_tg_consumer_with_bot(account_token, tg_chat_id):
    account = Account.objects.get(account_token=account_token)
    consumer = Consumer.objects.get(account=account, type=ConsumerType.TELEGRAM)
    consumer.data["tg_chat_id"] = tg_chat_id
    consumer.save()
    account.reset_account_token()
    account.save()
    success_tg_notification_activate.s(account.id).apply_async(
        task_id=f"success_activate_tg_notification for acc: {account.id}"
    )

import os

from celery_tasks.general_notification_tasks import success_notification_activated
from django.db import transaction
from notification.models import Consumer, ConsumerType
from utils.api_view_assistants import generate_new_account_token

TELEGRAM_BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]
VK_BOT_NUMBER = os.environ["VK_BOT_PUBLIC_NUMBER"].replace("public", "")


def create_telegram_join_url(account):
    generate_new_account_token(account)
    return {
        "join_url": f"https://t.me/{TELEGRAM_BOT_NAME}?start={account.account_token}"
    }


def create_vk_join_url(account):
    generate_new_account_token(account)
    return {
        "join_url": f"https://vk.com/im?sel=-{VK_BOT_NUMBER}&ref={account.account_token}"
    }


def add_recipient(account, **kwargs):
    recipient = kwargs["recipient"]
    consumer = Consumer.objects.get(account=account, type=ConsumerType.EMAIL)
    consumer.data["recipient"] = [recipient]
    consumer.save()

    success_notification_activated.s(account.id, "EMAIL").apply_async(
        task_id=f"email consumer ON - account: {account.id}"
    )
    return recipient


CONSUMER_ACTIVATE_DATA = {
    "TELEGRAM": create_telegram_join_url,
    "VK": create_vk_join_url,
    "EMAIL": add_recipient,
}


@transaction.atomic
def join_tg_consumer_with_bot(account, tg_chat_id):
    consumer = Consumer.objects.get(account=account, type=ConsumerType.TELEGRAM)
    consumer.data["tg_chat_id"] = tg_chat_id
    account.reset_account_token()
    consumer.save()
    account.save()


@transaction.atomic
def join_vk_consumer_with_bot(account, peer_id):
    consumer = Consumer.objects.get(account=account, type=ConsumerType.VK)
    consumer.data["peer_id"] = peer_id
    account.reset_account_token()
    consumer.save()
    account.save()

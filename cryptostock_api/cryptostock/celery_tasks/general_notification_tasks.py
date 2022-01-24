from account.models import Account
from celery import shared_task
from notification.models import Consumer, ConsumerType
from utils.notification_handlers.email_client import email_notify
from utils.notification_handlers.telegram_client import tg_notify


@shared_task
def success_tg_notification_activated(account_id):
    consumer = Consumer.objects.get(
        account=Account.objects.get(id=account_id), type=ConsumerType.TELEGRAM
    )
    tg_notify(
        message="<b>Notifications</b> for telegram have been <b>activated</b> .",
        context=consumer.data,
    )


@shared_task
def success_email_notification_activated(account_id):
    consumer = Consumer.objects.get(
        account=Account.objects.get(id=account_id), type=ConsumerType.EMAIL
    )
    email_notify(
        message="<b>Notifications</b> for email have been <b>activated</b> .",
        context=consumer.data,
    )

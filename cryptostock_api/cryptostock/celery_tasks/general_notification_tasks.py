from account.models import Account
from celery import shared_task
from notification.models import Consumer, ConsumerType
from utils.notification_handlers.telegram_client import tg_notify


@shared_task
def success_tg_notification_activate(account_id):
    consumer = Consumer.objects.get(
        account=Account.objects.get(id=account_id), type=ConsumerType.TELEGRAM
    )
    tg_notify(
        message="<b>Notifications</b> for telegram have been <b>activated</b> .",
        context=consumer.data,
    )

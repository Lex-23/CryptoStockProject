from account.models import Account
from celery import shared_task
from notification.models import SENDER, Consumer


@shared_task()
def success_notification_activated(account_id, consumer_type: str):
    consumer = Consumer.objects.get(
        account=Account.objects.get(id=account_id), type=consumer_type
    )
    SENDER[consumer_type](
        message=f"Notifications for {consumer_type} have been activated.",
        context=consumer.data,
    )

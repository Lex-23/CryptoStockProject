from account.models import Account
from celery import shared_task
from notification.models import TemplaterRegister


@shared_task
def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    if notification_type in account.enabled_notification_types:
        for consumer in account.enabled_consumers:
            templater = TemplaterRegister.get(notification_type, consumer.type)
            message = templater.render(data, notification_type)
            consumer.send(message)


@shared_task
def mul(x, y):
    return x * y

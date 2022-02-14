from account.models import Account
from notification.models import TemplaterRegister


def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    if notification_type in account.enabled_notification_types:
        for consumer in account.enabled_consumers:
            templater = TemplaterRegister.get(notification_type, consumer.type)
            message = templater.render(data, notification_type)
            consumer.send(message)

from account.models import Account
from notification.models import Notifier, TemplaterRegister


def notification_manager(account_id, **kwargs):
    active_account_notifiers = Notifier.objects.filter(
        account=Account.objects.get(id=account_id), active=True
    )
    for notifier in active_account_notifiers:
        notifier.type.send_notification(**kwargs)


def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    if notification_type in account.enabled_notification_types:
        for consumer in account.enabled_consumers:
            templater = TemplaterRegister.get(consumer.type, notification_type)
            message = templater.render(data)
            consumer.send(message, **data)

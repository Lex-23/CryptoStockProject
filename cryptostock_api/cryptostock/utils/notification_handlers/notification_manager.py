from account.models import Account
from notification.models import Notifier

from cryptostock_api.cryptostock.notification.models import Consumer, TemplaterRegister


def notification_manager(account_id, **kwargs):
    active_account_notifiers = Notifier.objects.filter(
        account=Account.objects.get(id=account_id), active=True
    )
    for notifier in active_account_notifiers:
        notifier.type.send_notification(**kwargs)


def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    enabled_consumers = Consumer.objects.get(account=account).enable_consumers
    if not enabled_consumers:
        pass

    for consumer in account.enabled_consumers:
        templater = TemplaterRegister.get(consumer.type, notification_type)
        message = templater.render(data)
        consumer.send(message, **data)

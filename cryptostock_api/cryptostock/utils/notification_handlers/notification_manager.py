from account.models import Account
from notification.models import Notifier


def notification_manager(account_id, **kwargs):
    active_account_notifiers = Notifier.objects.filter(
        account=Account.objects.get(id=account_id), active=True
    )
    for notifier in active_account_notifiers:
        notifier.type.send_notification(**kwargs)

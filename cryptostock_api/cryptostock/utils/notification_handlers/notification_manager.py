from account.models import Account
from notification.models import Notifier
from utils.notification_handlers.telegram_client import notify as tg_notify


def notification_manager(account_id, **kwargs):
    account = Account.objects.get(id=account_id)
    active_account_notifiers = Notifier.objects.filter(account=account, active=True)

    for notifier in active_account_notifiers:
        if notifier.type.client.NAME == "Telegram":
            notifier.type.client.send_notification(
                func=tg_notify,
                chat_id=notifier.telegram_chat_id,
                text=kwargs["tg_text"],
            ),
        else:
            # TODO: elif: other types notification
            pass

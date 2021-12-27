from account.models import Account
from django.db import models
from utils.notification_handlers.telegram_client import notify

_notifier_storage = {}


def notifier_register(name, notify_func):
    _notifier_storage[name] = notify_func
    return notify_func


tg_notify = notifier_register("Telegram", notify)


class NotificationType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    @property
    def notifier_func(self):
        notifier_func = _notifier_storage.get(self.name)
        if notifier_func is None:
            raise ValueError(f"Notifier with name {self.name} doesn't exist")
        return notifier_func

    def send_notification(self, **data):
        return self.notifier_func(**data)

    def __str__(self):
        return self.name


class Notifier(models.Model):
    """
    This is a universal model for set up types of users notifications
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    # TODO: add there FK to model with choice of notification event (may be)

    def __str__(self):
        return f"{self.type} for {self.account}"

    class Meta:
        unique_together = ("account", "type")

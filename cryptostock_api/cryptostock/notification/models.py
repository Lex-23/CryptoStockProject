import os

from account.models import Account
from django.db import models

_notifier_storage = {}


def notifier_register(cls):
    _notifier_storage[cls.NAME] = cls
    return cls


@notifier_register
class TelegramNotifier:
    NAME = "Telegram"

    @staticmethod
    def send_notification(func, chat_id, text, **kwargs):
        """
        method for notification in telegram
        :param text: notification text
        :param chat_id: personal users chat_id
        :param func: special func for send notification from telegram bot
        """
        return func(chat_id, text, **kwargs)


class NotificationType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    @property
    def notifier_cls(self):
        notifier_cls = _notifier_storage.get(self.name)
        if notifier_cls is None:
            raise ValueError(f"Notifier with name {self.name} doesn't exist")
        return notifier_cls

    @property
    def client(self):
        return self.notifier_cls

    def __str__(self):
        return self.name


class Notifier(models.Model):
    """
    This is a universal model for set up types of users notifications
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    telegram_chat_id = models.BigIntegerField(
        blank=True,
        null=True,
        help_text=f"input here 'chat_id' from telegram_bot {os.environ['TG_BOT_URL']}",
    )
    email = models.EmailField(
        blank=True, null=True, help_text="input here email you want for notifications"
    )
    active = models.BooleanField(default=True)
    # TODO: add other necessary attributes for other possible notifiers (skype, VK, etc)
    # TODO: add there FK to model with choice of notification event (may be)

    def __str__(self):
        return f"{self.type} for {self.account}"

    class Meta:
        unique_together = ("account", "type")

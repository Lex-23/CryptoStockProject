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
    def send_notification(func, text):
        """
        method for notification in telegram
        :param func: special func for send notification from telegram bot
        :param text: text for notification
        """
        return func(text)


class ManagerNotifier(models.Model):
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


class Notifier(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    notifier = models.ForeignKey(ManagerNotifier, on_delete=models.CASCADE)
    telegram_chat_id = models.BigIntegerField(
        blank=True,
        null=True,
        help_text=f"input here 'chat_id' from telegram_bot {os.environ['TG_BOT_URL']}",
    )
    email = models.EmailField(blank=True, null=True)

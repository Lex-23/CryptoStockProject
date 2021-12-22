from account.models import Account
from django.db import models


class TelegramNotifier(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    telegram_chat_id = models.BigIntegerField()

    def send_notification(self, func, text):
        """
        method for notification in telegram
        :param func: special func for send notification from telegram bot
        :param text: text for notification
        """
        return func(self.telegram_chat_id, text)

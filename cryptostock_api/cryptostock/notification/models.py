from enum import Enum
from typing import Any, Dict

from account.models import Account
from django.db import models
from utils.notification_handlers.email_client import email_notify
from utils.notification_handlers.telegram_client import tg_notify

_notifier_storage = {}


def notifier_register(name, notify_func):
    _notifier_storage[name] = notify_func
    return notify_func


notifier_register("Telegram", tg_notify)
notifier_register("Email", email_notify)


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


class ChoiceEnum(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((tag.value, tag.name) for tag in cls)


class ConsumerType(ChoiceEnum):
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"
    VK = "VK"


class NotificationEvent(ChoiceEnum):
    SUCCESS_OFFER = "SUCCESS_OFFER"
    SALESDASHBOARD_SOON_OVER = "SALESDASHBOARD_SOON_OVER"
    SALESDASHBOARD_IS_OVER = "SALESDASHBOARD_IS_OVER"


SENDER = {ConsumerType.TELEGRAM: tg_notify, ConsumerType.EMAIL: email_notify}


class Consumer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=ConsumerType.choices())
    data = models.JSONField(default=dict, blank=True)

    @property
    def enable_consumers(self):
        return Consumer.objects.all().filter(account=self.account, enable=True)

    def send(self, message, **data):
        return SENDER[self.type](message, **data)


class NotificationSubscription(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=50, choices=NotificationEvent.choices()
    )
    enable = models.BooleanField(default=True)

    @property
    def enable_notification_subscriptions(self):
        return NotificationSubscription.objects.all().filter(
            account=self.account, enable=True
        )


class TemplaterRegister:
    _templaters = {}

    @classmethod
    def register(cls, consumer_type, notification_type):
        def inner(templater_cls):
            # TODO: register logic
            return templater_cls

        return inner

    @classmethod
    def get(cls, consumer_type, notification_type):
        # TODO: get templator logic
        return cls._templaters.get(consumer_type, notification_type)


@TemplaterRegister.register(ConsumerType.TELEGRAM, NotificationEvent.SUCCESS_OFFER)
class BaseTemplator:
    def render(self, data: Dict[str, Any]) -> Any:
        return f"Event: {data}"

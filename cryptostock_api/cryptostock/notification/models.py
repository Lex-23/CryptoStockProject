from typing import Any, Dict, List

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


class ConsumerType:
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"


class NotificationEvent:
    SUCCESS_OFFER = "SUCCESS_OFFER"
    SALESDASHBOARD_SOON_OVER = "SALESDASHBOARD_SOON_OVER"
    SALESDASHBOARD_IS_OVER = "SALESDASHBOARD_IS_OVER"


class TemplaterRegister:
    _templaters = {}

    @classmethod
    def register(cls, consumer_type):
        def inner(templater_cls):
            cls._templaters[consumer_type] = templater_cls
            return templater_cls

        return inner

    get = classmethod(_templaters.get)


class BaseTemplator:
    def render(self, data: Dict[str]) -> Any:
        pass


@TemplaterRegister.register(ConsumerType.TELEGRAM)
class TelegramTemplator:
    def render(self, data: Dict[str, Any]) -> Any:
        return "Asset {asset} was sold to {client}".format(**data)


@TemplaterRegister.register(ConsumerType.EMAIL)
class EmailSoldAllTemplator:
    def render(self, data: Dict[str, Any]) -> Any:
        return "<p>Asset {asset} was sold to {client}</p>".format(**data)


SENDER = {ConsumerType.TELEGRAM: tg_notify, ConsumerType.EMAIL: email_notify}


class Consumer:
    user: int
    enable: bool
    type: ConsumerType
    data: Dict[str, Any]

    def send(self, message):
        return SENDER[self.type](message)


class NotificationSubscription:
    user: int
    notification_event: NotificationEvent
    enable: bool


class User:
    consumers: List[Consumer]
    notification_subscriptions: List[NotificationSubscription]


def notify(notification_type, user, data):
    if notification_type not in user.enabled_notification_subscriptions:
        return

    for consumer in user.enabled_consumers:
        templater = TemplaterRegister.get((consumer.type, notification_type))
        message = templater.render(data)
        consumer.send(message)

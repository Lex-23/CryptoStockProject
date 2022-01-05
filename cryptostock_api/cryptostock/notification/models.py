from enum import Enum
from typing import Any, Dict

from account.models import Account, Offer, SalesDashboard
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
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="consumers"
    )
    enable = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=ConsumerType.choices())
    data = models.JSONField(default=dict, blank=True)

    def send(self, message):
        sender = SENDER.get(self.type)
        if sender is None:
            raise ValueError(f"Sender doesn't exist, type={self.type}")
        return sender(message, context=self.data)

    def __str__(self):
        return self.type


class NotificationSubscription(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="notification_subscriptions"
    )
    notification_type = models.CharField(
        max_length=50, choices=NotificationEvent.choices()
    )
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.notification_type


class TemplaterRegister:
    _templaters = {}

    @classmethod
    def register(cls, notification_type, consumer_type=None):
        def inner(templater_cls):
            cls._templaters[notification_type, consumer_type] = templater_cls
            return templater_cls

        return inner

    @classmethod
    def get(cls, notification_type, consumer_type):
        return cls._templaters.get(
            (notification_type, consumer_type),
            cls._templaters.get((notification_type, None), BaseTemplater),
        )


class BaseTemplater:
    @staticmethod
    def render(data: Dict[str, Any], notification_type) -> Any:
        return f"Happened {notification_type} with info: {data}."


@TemplaterRegister.register(notification_type=NotificationEvent.SUCCESS_OFFER)
class SuccessOfferTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        return (
            f"User {offer.client.owner.username} bought from you {offer.count} "
            f"{offer.deal.asset.name}\nfor total value: {offer.total_value} in {offer.timestamp.date()}.\n"
            f"Buyer email: {offer.client.owner.email}."
        )


@TemplaterRegister.register(
    notification_type=NotificationEvent.SALESDASHBOARD_SOON_OVER
)
class SalesDashboardSoonOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        return (
            f"Your asset {offer.deal.asset.name} on sales dashboard #{offer.deal.id}\n"
            f"soon will be over, {offer.deal.count} remain."
        )


@TemplaterRegister.register(notification_type=NotificationEvent.SALESDASHBOARD_IS_OVER)
class SalesDashboardIsOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        salesdashboard = SalesDashboard.objects.get(id=data["deal_id"])
        return f"Your sales dashboard #{salesdashboard.id} with {salesdashboard.asset.name} sold completely."


@TemplaterRegister.register(
    notification_type=NotificationEvent.SUCCESS_OFFER, consumer_type=ConsumerType.EMAIL
)
class SuccessOfferEmailTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        message = {
            "recipient": (f"{offer.deal.broker.owner.email}",),
            "subject": "You received successful offer from your sales dashboard.",
            "body": f"Hello, {offer.deal.broker.owner.username}.\n"
            f"User {offer.client.owner.username} bought from you {offer.count} "
            f"{offer.deal.asset.name} for total value: {offer.total_value} in {offer.timestamp.date()}.\n"
            f"Buyer email: {offer.client.owner.email}.",
        }
        return message

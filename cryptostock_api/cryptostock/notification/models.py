from enum import Enum
from typing import Any, Dict

from account.models import Account, Offer, SalesDashboard
from django.db import models
from utils.notification_handlers.email_client import email_notify
from utils.notification_handlers.telegram_client import tg_notify
from utils.notification_handlers.vk_client import vk_notify


class ChoiceEnum(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((tag.value, tag.name) for tag in cls)


class ConsumerType(ChoiceEnum):
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"
    VK = "VK"


class NotificationType(ChoiceEnum):
    SUCCESS_OFFER = "SUCCESS_OFFER"
    SALESDASHBOARD_SOON_OVER = "SALESDASHBOARD_SOON_OVER"
    SALESDASHBOARD_IS_OVER = "SALESDASHBOARD_IS_OVER"


SENDER = {
    ConsumerType.TELEGRAM: tg_notify,
    ConsumerType.EMAIL: email_notify,
    ConsumerType.VK: vk_notify,
}


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

    class Meta:
        unique_together = ("account", "type")


class NotificationSubscription(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="notification_subscriptions"
    )
    notification_type = models.CharField(
        max_length=50, choices=NotificationType.choices()
    )
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.notification_type

    class Meta:
        unique_together = ("account", "notification_type")


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
        return (
            cls._templaters.get((notification_type, consumer_type))
            or cls._templaters.get((notification_type, None))
            or BaseTemplater
        )


class BaseTemplater:
    @staticmethod
    def render(data: Dict[str, Any], notification_type) -> Any:
        return f"Happened {notification_type} with info: {data}."


@TemplaterRegister.register(notification_type=NotificationType.SUCCESS_OFFER)
class SuccessOfferTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        return (
            f"User {offer.client.owner.username} bought from you <b>{offer.count} "
            f"{offer.asset.name}\n</b>for total value: <b>{offer.total_value}</b> in {offer.timestamp.date()}.\n"
            f"Buyer email: {offer.client.owner.email}."
        )


@TemplaterRegister.register(notification_type=NotificationType.SALESDASHBOARD_SOON_OVER)
class SalesDashboardSoonOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        sale = SalesDashboard.objects.get(id=data["salesdashboard_id"])
        return (
            f"Your asset <b>{sale.asset.name}</b> on sales dashboard #{sale.id}\n"
            f"<b>soon will be over</b>, {sale.count} remain."
        )


@TemplaterRegister.register(notification_type=NotificationType.SALESDASHBOARD_IS_OVER)
class SalesDashboardIsOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        return f"Your sales dashboard #{data['deal_id']} with <b>{data['asset_name']} sold completely</b>."


@TemplaterRegister.register(
    notification_type=NotificationType.SUCCESS_OFFER, consumer_type=ConsumerType.EMAIL
)
class SuccessOfferEmailTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        return {
            "subject": "You received successful offer from your sales dashboard.",
            "body": f"<h2>Hello, {offer.broker.owner.username}.</h2>"
            f"<p>User {offer.client.owner.username} bought from you <b>{offer.count} "
            f"{offer.asset.name}</b> for total value: "
            f"<b>{offer.total_value}</b> in {offer.timestamp.date()}.</p>"
            f"<h4>Buyer email: {offer.client.owner.email}.</h4>",
        }

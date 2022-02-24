from enum import Enum
from typing import Any, Dict

from account.models import Account, Broker, Client, Offer, SalesDashboard
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


class BrokerNotificationType(ChoiceEnum):
    SUCCESS_OFFER = "SUCCESS_OFFER"
    SALESDASHBOARD_SOON_OVER = "SALESDASHBOARD_SOON_OVER"
    SALESDASHBOARD_IS_OVER = "SALESDASHBOARD_IS_OVER"
    ASSET_APPEARED_ON_MARKET = "ASSET_APPEARED_ON_MARKET"
    ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET = "ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET"
    ASSET_PRICE_HAS_BEEN_RICED_ON_MARKET = "ASSET_PRICE_HAS_BEEN_RICED_ON_MARKET"


class ClientNotificationType(ChoiceEnum):
    NEW_SALESDASHBOARD = "NEW_SALESDASHBOARD"
    ASSET_PRICE_HAS_BEEN_DROPPED = "ASSET_PRICE_HAS_BEEN_DROPPED"


# When we created new schedule notification tasks - required add them to this list
SCHEDULE_MARKET_NOTIFICATION_TYPES = [
    BrokerNotificationType.ASSET_APPEARED_ON_MARKET,
    BrokerNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET,
    BrokerNotificationType.ASSET_PRICE_HAS_BEEN_RICED_ON_MARKET,
]


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
    notification_type = models.CharField(null=True, blank=True)
    enable = models.BooleanField(default=True)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.notification_type

    class Meta:
        abstract = True
        unique_together = ("account", "notification_type")

    @classmethod
    def get_all_enable_subscriptions_filter_by_type(cls, notification_type):
        return cls.objects.filter(notification_type=notification_type, enable=True)


class BrokerNotificationSubscription(NotificationSubscription):
    account = models.ForeignKey(
        Broker, on_delete=models.CASCADE, related_name="notification_subscriptions"
    )
    notification_type = models.CharField(
        max_length=100, choices=BrokerNotificationType.choices()
    )

    @staticmethod
    def get_all_enable_schedule_notification_subscriptions():
        return BrokerNotificationSubscription.objects.filter(
            notification_type__in=SCHEDULE_MARKET_NOTIFICATION_TYPES, enable=True
        )


class ClientNotificationSubscription(NotificationSubscription):
    account = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="notification_subscriptions"
    )
    notification_type = models.CharField(
        max_length=100, choices=ClientNotificationType.choices()
    )


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
        print(f"DATA: {data}")
        return f"Happened {notification_type} with info: {data}."


@TemplaterRegister.register(notification_type=BrokerNotificationType.SUCCESS_OFFER)
class SuccessOfferTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        offer = Offer.objects.get(id=data["offer_id"])
        return (
            f"User {offer.client.owner.username} bought from you <b>{offer.count} "
            f"{offer.asset.name}\n</b>for total value: <b>{offer.total_value}</b> in {offer.timestamp.date()}.\n"
            f"Buyer email: {offer.client.owner.email}."
        )


@TemplaterRegister.register(
    notification_type=BrokerNotificationType.SALESDASHBOARD_SOON_OVER
)
class SalesDashboardSoonOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        sale = SalesDashboard.objects.get(id=data["salesdashboard_id"])
        return (
            f"Your asset <b>{sale.asset.name}</b> on sales dashboard #{sale.id}\n"
            f"<b>soon will be over</b>, {sale.count} remain."
        )


@TemplaterRegister.register(
    notification_type=BrokerNotificationType.SALESDASHBOARD_IS_OVER
)
class SalesDashboardIsOverTemplater:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        return f"Your sales dashboard #{data['deal_id']} with <b>{data['asset_name']} sold completely</b>."


@TemplaterRegister.register(notification_type=ClientNotificationType.NEW_SALESDASHBOARD)
class UpdateAssetOnSalesDashboard:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        sale = SalesDashboard.objects.get(id=data["sale_id"])
        return (
            f"We have <b>updates</b> for your tracked asset <b>{sale.asset.name}</b>.\n"
            f"Info about new salesdashboard with <b>id: {sale.id}</b>:\n"
            f"<b>price: {sale.price}</b>, <b>count: {sale.count}</b>."
        )


@TemplaterRegister.register(
    notification_type=ClientNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED
)
class PriceAssetHasBeenDropped:
    @staticmethod
    def render(data: Dict[str, Any], *args) -> Any:
        sale = SalesDashboard.objects.get(id=data["sale_id"])
        return (
            f"We have asset <b>{sale.asset.name}</b> which price has been dropped.\n"
            f"Info: salesdashboard with <b>id: {sale.id}</b>:\n"
            f"<b>price: {sale.price}</b>, <b>count: {sale.count}</b>."
        )


@TemplaterRegister.register(
    notification_type=BrokerNotificationType.ASSET_PRICE_HAS_BEEN_RICED_ON_MARKET
)
@TemplaterRegister.register(
    notification_type=BrokerNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET
)
@TemplaterRegister.register(
    notification_type=BrokerNotificationType.ASSET_APPEARED_ON_MARKET
)
class AssetAppearedOnMarket:
    @staticmethod
    def render(data: Dict[str, Any], notification_type) -> Any:
        assets_info = data.get("assets_info")
        result_list = []
        for market, assets in assets_info.items():
            for name, price in assets.items():
                result_list.append(f"<b>{market}</b> - {name}: <b>{price}</b>. \n")
        return (
            f"We have update info about assets from markets for you:\n{''.join(result_list)}"
            f"event: {notification_type}"
        )


@TemplaterRegister.register(
    notification_type=BrokerNotificationType.SUCCESS_OFFER,
    consumer_type=ConsumerType.EMAIL,
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

import decimal
from dataclasses import dataclass

from account.models import Account
from notification.models import NotificationSubscription, TemplaterRegister


def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    if notification_type in account.enabled_notification_types:
        for consumer in account.enabled_consumers:
            templater = TemplaterRegister.get(notification_type, consumer.type)
            message = templater.render(data, notification_type)
            consumer.send(message)


@dataclass
class TrackedAsset:
    name: str
    min_price: decimal.Decimal = None
    max_price: decimal.Decimal = None

    def __str__(self):
        return self.name

    @property
    def track_only_asset_name(self):
        return self.min_price is None and self.max_price is None


def notify_scope_of_clients(notification_type, **data):
    for (
        notification_subscription
    ) in NotificationSubscription.get_all_enable_subscriptions_filter_by_type(
        notification_type
    ):
        if data["asset_name"] in [asset.name for asset in data["tracked_assets"]]:
            target = next(
                asset
                for asset in data["tracked_assets"]
                if asset.name == data["asset_name"]
            )
            if target.track_only_asset_name:
                notify(notification_type, notification_subscription.account.id, **data)

import decimal

from account.models import SalesDashboard
from celery import shared_task
from django.db import transaction
from notification.models import ClientNotificationSubscription, ClientNotificationType
from utils.notification_handlers.common_services import notify


def notify_scope_of_clients_new_salesdashboard(**data):
    notification_type = ClientNotificationType.NEW_SALESDASHBOARD
    sale = SalesDashboard.objects.get(id=data["sale_id"])
    filter_queryset = ClientNotificationSubscription.get_all_enable_subscriptions_filter_by_type(
        notification_type
    ).filter(
        data__tracked_assets__contains=sale.asset.name
    )
    for notification_subscription in filter_queryset:
        notify(notification_type, notification_subscription.account.id, **data)


def notify_scope_of_clients_asset_price_dropped(**data):
    notification_type = ClientNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED
    sale = SalesDashboard.objects.get(id=data["sale_id"])
    filter_queryset = ClientNotificationSubscription.get_all_enable_subscriptions_filter_by_type(
        notification_type
    ).filter(
        data__min_tracked_price__has_key=sale.asset.name
    )
    for notification_subscription in filter_queryset:
        if sale.price <= decimal.Decimal(
            notification_subscription.data["tracked_price"][sale.asset.name]
        ):
            notify(notification_type, notification_subscription.account.id, **data)


NOTIFY_SCOPE_OF_CLIENTS = {
    ClientNotificationType.NEW_SALESDASHBOARD: notify_scope_of_clients_new_salesdashboard,
    ClientNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED: notify_scope_of_clients_asset_price_dropped,
}


@shared_task
def async_notify_for_scope_of_clients(notification_type, **data):
    return NOTIFY_SCOPE_OF_CLIENTS[notification_type](**data)


def async_notify_clients_update_on_salesdashboard(sale_id, notification_type):
    transaction.on_commit(
        lambda: async_notify_for_scope_of_clients.s(
            sale_id=sale_id, notification_type=notification_type
        ).apply_async(
            task_id=f"notification for scope of clients by salesdasboard: {sale_id}"
        )
    )

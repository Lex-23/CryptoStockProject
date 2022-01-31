from account.models import SalesDashboard
from celery import shared_task
from django.db import transaction
from notification.models import NotificationSubscription, NotificationType
from utils.notification_handlers.common_services import notify


def notify_scope_of_clients_about_new_salesdashboard(**data):
    notification_type = NotificationType.NEW_SALESDASHBOARD
    sale = SalesDashboard.objects.get(id=data["sale_id"])
    for (
        notification_subscription
    ) in NotificationSubscription.get_all_enable_subscriptions_filter_by_type(
        notification_type
    ).filter(
        data__tracked_assets__contains=sale.asset.name
    ):
        notify(notification_type, notification_subscription.account.id, **data)


@shared_task
def async_notify_for_client(**data):
    return notify_scope_of_clients_about_new_salesdashboard(**data)


def async_notify_clients_new_salesdashboard(sale_id):
    transaction.on_commit(
        lambda: async_notify_for_client.s(sale_id=sale_id).apply_async(
            task_id=f"client's notification for salesdasboard: {sale_id}"
        )
    )

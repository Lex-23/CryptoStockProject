from celery import shared_task
from django.db import transaction
from notification.models import NotificationType
from utils.notification_handlers.common_services import notify


@shared_task
def async_notify_for_broker(notification_type, account_id, **data):
    return notify(notification_type, account_id, **data)


def async_notify_success_offer(offer):
    transaction.on_commit(
        lambda: async_notify_for_broker.s(
            notification_type=NotificationType.SUCCESS_OFFER,
            account_id=offer.broker.id,
            offer_id=offer.id,
        ).apply_async(task_id=f"offer_success notification: {offer.id}")
    )


def async_notify_salesdashboard_soon_over(offer, deal):
    transaction.on_commit(
        lambda: async_notify_for_broker.s(
            notification_type=NotificationType.SALESDASHBOARD_SOON_OVER,
            account_id=offer.broker.id,
            salesdashboard_id=deal.id,
        ).apply_async(task_id=f"salesdashboard soon_over notification: {deal.id}")
    )


def async_notify_salesdashboard_is_over(broker, deal_id, asset_name):
    transaction.on_commit(
        lambda: async_notify_for_broker.s(
            notification_type=NotificationType.SALESDASHBOARD_IS_OVER,
            account_id=broker.id,
            deal_id=deal_id,
            asset_name=asset_name,
        ).apply_async(task_id=f"salesdashboard_is_over notification: {deal_id}")
    )

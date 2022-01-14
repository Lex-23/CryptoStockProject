from account.models import Account
from celery import shared_task
from django.db import transaction
from notification.models import NotificationType, TemplaterRegister


@shared_task
def notify(notification_type, account_id, **data):
    account = Account.objects.get(id=account_id)
    if notification_type in account.enabled_notification_types:
        for consumer in account.enabled_consumers:
            templater = TemplaterRegister.get(notification_type, consumer.type)
            message = templater.render(data, notification_type)
            consumer.send(message)


def async_notify_success_offer(offer):
    transaction.on_commit(
        lambda: notify.s(
            notification_type=NotificationType.SUCCESS_OFFER,
            account_id=offer.broker.id,
            offer_id=offer.id,
        ).apply_async(task_id=f"offer_success notification: {offer.id}")
    )


def async_notify_salesdashboard_soon_over(offer, deal):
    transaction.on_commit(
        lambda: notify.s(
            notification_type=NotificationType.SALESDASHBOARD_SOON_OVER,
            account_id=offer.broker.id,
            salesdashboard_id=deal.id,
        ).apply_async(task_id=f"salesdashboard soon_over notification: {deal.id}")
    )


def async_notify_salesdashboard_is_over(broker, deal_id, asset_name):
    transaction.on_commit(
        lambda: notify.s(
            notification_type=NotificationType.SALESDASHBOARD_IS_OVER,
            account_id=broker.id,
            deal_id=deal_id,
            asset_name=asset_name,
        ).apply_async(task_id=f"salesdashboard_is_over notification: {deal_id}")
    )

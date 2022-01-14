from unittest.mock import call, patch

import pytest
from account.tests.factory import OfferFactory, SalesDashboardFactory
from celery_tasks.broker_notification_tasks import notify
from django.conf import settings
from notification.models import ConsumerType, NotificationType, TemplaterRegister
from notification.tests.factory import ConsumerFactory, NotificationSubscriptionFactory
from utils.notification_handlers.email_client import CRYPTOSTOCK_NAME


@pytest.mark.parametrize(
    "notification_type",
    [
        NotificationType.SUCCESS_OFFER,
        NotificationType.SALESDASHBOARD_IS_OVER,
        NotificationType.SALESDASHBOARD_SOON_OVER,
    ],
)
@patch(
    "utils.notification_handlers.telegram_client.bot.send_message",
    return_value="success telegram notify",
)
def test_telegram_notify_success(send_message, notification_type):
    salesdasboard = SalesDashboardFactory()
    offer = OfferFactory(asset=salesdasboard.asset, broker=salesdasboard.broker)
    data = {
        NotificationType.SUCCESS_OFFER: {"offer_id": offer.id},
        NotificationType.SALESDASHBOARD_IS_OVER: {
            "deal_id": salesdasboard.id,
            "asset_name": salesdasboard.asset.name,
        },
        NotificationType.SALESDASHBOARD_SOON_OVER: {
            "salesdashboard_id": salesdasboard.id
        },
    }
    account = salesdasboard.broker

    consumer = ConsumerFactory(
        account=account, type=ConsumerType.TELEGRAM, data={"tg_chat_id": 00000000}
    )
    notification_subscription = NotificationSubscriptionFactory(
        account=account, notification_type=notification_type
    )
    notify(
        notification_type=notification_type,
        account_id=account.id,
        **data[notification_type],
    )

    templater = TemplaterRegister.get(
        notification_subscription.notification_type, consumer.type
    )
    message = templater.render(
        data[notification_type], notification_subscription.notification_type
    )

    assert send_message.called is True
    assert send_message.call_args == call(
        consumer.data["tg_chat_id"], message, parse_mode="html"
    )


@pytest.mark.parametrize(
    "notification_type",
    [
        NotificationType.SUCCESS_OFFER,
        NotificationType.SALESDASHBOARD_IS_OVER,
        NotificationType.SALESDASHBOARD_SOON_OVER,
    ],
)
@patch(
    "utils.notification_handlers.email_client.send_mail",
    return_value="success email notify",
)
def test_email_notify_success(send_mail, notification_type):
    salesdasboard = SalesDashboardFactory()
    offer = OfferFactory(asset=salesdasboard.asset, broker=salesdasboard.broker)
    data = {
        NotificationType.SUCCESS_OFFER: {"offer_id": offer.id},
        NotificationType.SALESDASHBOARD_IS_OVER: {
            "deal_id": salesdasboard.id,
            "asset_name": salesdasboard.asset.name,
        },
        NotificationType.SALESDASHBOARD_SOON_OVER: {
            "salesdashboard_id": salesdasboard.id
        },
    }
    account = salesdasboard.broker

    consumer = ConsumerFactory(
        account=account, type=ConsumerType.EMAIL, data={"recipient": ["mail@mail.mail"]}
    )
    notification_subscription = NotificationSubscriptionFactory(
        account=account, notification_type=notification_type
    )
    notify(
        notification_type=notification_type,
        account_id=account.id,
        **data[notification_type],
    )

    templater = TemplaterRegister.get(
        notification_subscription.notification_type, consumer.type
    )
    message = templater.render(
        data[notification_type], notification_subscription.notification_type
    )
    subject = f"Notification from {CRYPTOSTOCK_NAME}"
    if isinstance(message, dict):
        subject = message["subject"]
        message = message["body"]

    assert send_mail.called is True
    assert send_mail.call_args == call(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        consumer.data["recipient"],
        html_message=message,
        fail_silently=False,
    )

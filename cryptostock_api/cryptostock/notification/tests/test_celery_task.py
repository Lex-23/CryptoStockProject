import decimal as d
from unittest.mock import patch

from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)
from notification.models import ConsumerType, NotificationType
from notification.tests.factory import ConsumerFactory, NotificationSubscriptionFactory


@patch("celery_tasks.broker_notification_tasks.notify", return_value="success notify")
@patch(
    "utils.api_view_assistants.async_notify_success_offer",
    return_value="success notify",
)
def test_success_offer_notification(async_notify_success_offer, auth_client):
    broker = BrokerFactory(cash_balance=d.Decimal("1000.00"))
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("150.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset, broker=broker, success_offer_notification=True
    )

    consumer = ConsumerFactory(account=broker, type=ConsumerType.EMAIL)
    NotificationSubscriptionFactory(
        account=consumer.account, notification_type=NotificationType.SUCCESS_OFFER
    )

    # @patch('celery_tasks.broker_notification_tasks.notify')
    # def notify():
    #     return 'success notify'
    # #

    data = {"count": "2"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)
    breakpoint()
    assert response.status_code == 201
    assert async_notify_success_offer.called is True
    # assert notify.called is True

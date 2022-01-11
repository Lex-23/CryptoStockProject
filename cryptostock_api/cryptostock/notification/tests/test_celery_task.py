# import decimal as d
# from unittest.mock import MagicMock
#
# import pytest
# from account.tests.factory import (
#     BrokerFactory,
#     SalesDashboardFactory,
#     WalletRecordFactory,
# )
# from notification.models import ConsumerType, NotificationType
# from notification.tests.factory import ConsumerFactory, NotificationSubscriptionFactory
#
#
# def test_success_offer_notification(auth_client, client_account, celeryapp):
#     broker = BrokerFactory(cash_balance=d.Decimal("1000.00"))
#     client = client_account
#     wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("150.00"))
#     sale = SalesDashboardFactory(
#         asset=wallet_record.asset, broker=broker, success_offer_notification=True
#     )
#
#     consumer = ConsumerFactory(account=broker, type=ConsumerType.EMAIL)
#     notification_subscription = NotificationSubscriptionFactory(
#         account=consumer.account, notification_type=NotificationType.SUCCESS_OFFER
#     )
#     consumer.send = MagicMock(return_value="success notify")
#     notify = MagicMock(return_value="success notify")
#
#     data = {"count": "2"}
#
#     response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)
#
#     assert response.status_code == 201
#     breakpoint()
#     assert consumer.send.called is True

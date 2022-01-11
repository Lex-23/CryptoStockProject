# from unittest.mock import MagicMock
#
# from notification.models import ConsumerType, NotificationType
# from notification.tests.factory import (
#     AccountFactory,
#     ConsumerFactory,
#     NotificationSubscriptionFactory,
# )
#
#
# def test_notify():
#     account = AccountFactory()
#     tg_notify = MagicMock(return_value="success notify")
#     consumer = ConsumerFactory(account=account, type=ConsumerType.TELEGRAM)
#     notification_subscription = NotificationSubscriptionFactory(
#         account=account, notification_type=NotificationType.SUCCESS_OFFER
#     )

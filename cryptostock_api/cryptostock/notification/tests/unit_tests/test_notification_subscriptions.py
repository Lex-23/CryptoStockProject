from notification.models import NotificationSubscription
from notification.tests.factory import NotificationSubscriptionFactory


def test_get_all_enable_subscriptions_filter_by_type():
    NotificationSubscriptionFactory.create_batch(
        5, notification_type="TARGET_ASSET_ON_SALESDASHBOAD"
    )
    NotificationSubscriptionFactory(
        notification_type="TARGET_ASSET_ON_SALESDASHBOAD", enable=False
    )
    NotificationSubscriptionFactory(notification_type="SUCCESS_OFFER", enable=False)

    expect = NotificationSubscription.get_all_enable_subscriptions_filter_by_type(
        notification_type="TARGET_ASSET_ON_SALESDASHBOAD"
    )
    breakpoint()
    assert len(expect) == 5

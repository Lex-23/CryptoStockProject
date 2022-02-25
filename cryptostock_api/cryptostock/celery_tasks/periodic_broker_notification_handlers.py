import json

from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from market.models import Market
from notification.models import BrokerNotificationSubscription, BrokerNotificationType
from utils.notification_handlers.common_services import notify
from utils.notification_handlers.market_info_parser import MarketInfoParser


def retrieve_assets_from_market():
    for market in Market.objects.all():
        market.kwargs["last_update_info"] = market.client.get_assets()
        market.save()


def notify_broker_asset_appeared_on_market(broker_id, sub_id):
    sub = BrokerNotificationSubscription.objects.get(id=sub_id)
    asset_list = sub.data["tracked_assets"]

    parser = MarketInfoParser()
    parser.get_assets_by_list(asset_list)
    assets_info = parser.get_info_not_null
    if assets_info:
        notify(
            notification_type=BrokerNotificationType.ASSET_APPEARED_ON_MARKET,
            account_id=broker_id,
            assets_info=assets_info,
        )


def notify_broker_asset_has_been_dropped_on_market(broker_id, sub_id):
    sub = BrokerNotificationSubscription.objects.get(id=sub_id)
    asset_dict = sub.data["min_asset_price"]

    parser = MarketInfoParser()
    assets_info = parser.get_assets_by_dict(asset_dict, key="min_asset_price")
    if assets_info:
        notify(
            notification_type=BrokerNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET,
            account_id=broker_id,
            assets_info=assets_info,
        )


def notify_broker_asset_has_been_raised_on_market(broker_id, sub_id):
    sub = BrokerNotificationSubscription.objects.get(id=sub_id)
    asset_dict = sub.data["max_asset_price"]

    parser = MarketInfoParser()
    assets_info = parser.get_assets_by_dict(asset_dict, key="max_asset_price")
    if assets_info:
        notify(
            notification_type=BrokerNotificationType.ASSET_PRICE_HAS_BEEN_RAISED_ON_MARKET,
            account_id=broker_id,
            assets_info=assets_info,
        )


PERIODIC_TASKS = {
    BrokerNotificationType.ASSET_APPEARED_ON_MARKET:
        "celery_tasks.schedule_tasks.periodic_notify_broker_asset_appeared_on_market",
    BrokerNotificationType.ASSET_PRICE_HAS_BEEN_DROPPED_ON_MARKET:
        "celery_tasks.schedule_tasks.periodic_notify_broker_asset_has_been_dropped_on_market",
    BrokerNotificationType.ASSET_PRICE_HAS_BEEN_RAISED_ON_MARKET:
        "celery_tasks.schedule_tasks.periodic_notify_broker_asset_has_been_raised_on_market",
}


def create_periodic_task_broker(
    notification_type, broker_id, sub_id, period="minutes", period_count=480
):
    PeriodicTask.objects.create(
        name=f"Periodic notify broker {broker_id} for {notification_type}",
        task=PERIODIC_TASKS[notification_type],
        interval=IntervalSchedule.objects.get(every=period_count, period=period),
        start_time=timezone.now(),
        args=json.dumps([broker_id, sub_id]),
    )

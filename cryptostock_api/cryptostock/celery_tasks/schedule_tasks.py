from celery import shared_task
from django.db import transaction
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from market.models import Market
from notification.models import BrokerNotificationSubscription, BrokerNotificationType
from utils.notification_handlers.common_services import notify


def retrieve_assets_from_market():
    for market in Market.objects.all():
        market.kwargs["last_update_info"] = market.client.get_assets()
        market.save()


@shared_task
def scan_markets():
    return retrieve_assets_from_market()


def parse_market_for_assets(asset_list: list):
    info = {}
    for market in Market.objects.all():
        info[market.name] = {}
        for asset_name in asset_list:
            for asset in market.kwargs["last_update_info"]:
                if asset["name"] == asset_name:
                    info[market.name][asset_name] = asset["price"]

    res_info = dict((key, value) for key, value in info.items() if value)
    return res_info


def notify_broker_asset_on_market(broker_id, sub_id):
    sub = BrokerNotificationSubscription.objects.get(id=sub_id)
    asset_list = sub.data["tracked_assets"]
    assets_info = parse_market_for_assets(asset_list)
    if assets_info:
        notify(
            notification_type=BrokerNotificationType.ASSET_APPEARED_ON_MARKET,
            account_id=broker_id,
            assets_info=assets_info,
        )


@shared_task
def async_notify_broker_asset_on_market(broker_id, sub_id):
    return notify_broker_asset_on_market(broker_id, sub_id)


@shared_task(name="periodic_notify_broker_asset_on_market")
def periodic_notify_broker_asset_on_market(broker_id, sub_id):
    transaction.on_commit(
        lambda: async_notify_broker_asset_on_market.s(broker_id, sub_id).apply_async(
            task_id=f"notify broker {broker_id} - asset on market"
        )
    )


PERIODIC_TASKS = {
    BrokerNotificationType.ASSET_APPEARED_ON_MARKET: periodic_notify_broker_asset_on_market
}


def create_periodic_task_broker(notification_type, broker_id):
    PeriodicTask.objects.create(
        name=f"Periodic notify broker {broker_id} for {notification_type}",
        task=f"{PERIODIC_TASKS[notification_type]}",
        interval=IntervalSchedule.objects.get(every=12, period="hours"),
        start_time=timezone.now(),
    )
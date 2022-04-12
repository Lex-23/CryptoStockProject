from celery import shared_task
from celery_tasks.periodic_broker_notification_handlers import (
    notify_broker_asset_appeared_on_market,
    notify_broker_asset_has_been_dropped_on_market,
    notify_broker_asset_has_been_raised_on_market,
    retrieve_assets_from_market,
)
from django.db import transaction

scan_markets = shared_task(name="celery_tasks.schedule_tasks.scan_markets")(
    retrieve_assets_from_market
)


@shared_task
def async_notify_broker_asset_appeared_on_market(broker_id, sub_id):
    return notify_broker_asset_appeared_on_market(broker_id, sub_id)


@shared_task
def async_notify_broker_asset_has_been_dropped_on_market(broker_id, sub_id):
    return notify_broker_asset_has_been_dropped_on_market(broker_id, sub_id)


@shared_task
def async_notify_broker_asset_has_been_raised_on_market(broker_id, sub_id):
    return notify_broker_asset_has_been_raised_on_market(broker_id, sub_id)


@shared_task(
    name="celery_tasks.schedule_tasks.periodic_notify_broker_asset_appeared_on_market"
)
def periodic_notify_broker_asset_on_market(broker_id, sub_id):
    transaction.on_commit(
        lambda: async_notify_broker_asset_appeared_on_market.s(
            broker_id, sub_id
        ).apply_async(task_id=f"notify broker {broker_id} - asset on market")
    )


@shared_task(
    name="celery_tasks.schedule_tasks.periodic_notify_broker_asset_has_been_dropped_on_market"
)
def periodic_notify_broker_asset_has_been_dropped_on_market(broker_id, sub_id):
    transaction.on_commit(
        lambda: async_notify_broker_asset_has_been_dropped_on_market.s(
            broker_id, sub_id
        ).apply_async(
            task_id=f"notify broker {broker_id} - asset has been dropped on market"
        )
    )


@shared_task(
    name="celery_tasks.schedule_tasks.periodic_notify_broker_asset_has_been_raised_on_market"
)
def periodic_notify_broker_asset_has_been_raised_on_market(broker_id, sub_id):
    transaction.on_commit(
        lambda: async_notify_broker_asset_has_been_raised_on_market.s(
            broker_id, sub_id
        ).apply_async(
            task_id=f"notify broker {broker_id} - asset has been raised on market"
        )
    )

from celery import shared_task
from market.models import Market


def retrieve_assets_from_market():
    result_info = {}
    for market in Market.objects.all():
        result_info[market.name] = market.client.get_assets()
    return result_info


@shared_task(bind=True)
def scan_market():
    print(retrieve_assets_from_market)
    return retrieve_assets_from_market()

import decimal

from account.models import Offer, PurchaseDashboard, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from asset.models import Asset
from celery_tasks.broker_notification_tasks import notify
from django.db import transaction
from notification.models import NotificationType
from utils import validators
from utils.validators import (
    get_validated_asset_from_market,
    validate_broker_cash_balance,
)
from wallet.models import WalletRecord


def create_sale_object_serializer(count, price, asset, broker, **kwargs) -> dict:
    """
    Validate request, create and serialize new object of SalesDashboard
    """
    validators.validate_asset_exists(asset, broker)
    validators.validate_asset_count(count, asset, broker)

    new_object = SalesDashboard.objects.create(
        asset=asset, broker=broker, count=count, price=price, **kwargs
    )
    serializer = SalesDashboardSerializer(new_object)
    return serializer.data


def _broker_sale_asset(broker, deal, count, value):
    """
    Update broker`s cash_balance and wallet_record after offer
    """
    broker_wallet_record = broker.wallet.wallet_record.get(asset=deal.asset)
    broker_wallet_record.count -= count
    broker_wallet_record.save()
    broker.cash_balance += value
    broker.save()


def _is_asset_exists_in_wallet(deal, client):
    asset = deal.asset
    return client.wallet.wallet_record.filter(asset=asset).exists()


def _client_buy_asset(client, deal, count, value):
    """
    Update clients`s cash_balance and wallet_record after offer
    """
    if _is_asset_exists_in_wallet(deal, client):
        client_wallet_record = client.wallet.wallet_record.get(asset=deal.asset)
        client_wallet_record.count += count
        client_wallet_record.save()
    else:
        WalletRecord.objects.create(asset=deal.asset, wallet=client.wallet, count=count)
    client.cash_balance -= value
    client.save()


def deal_flow(client, deal, count, value):
    """
    This func changes brokers` and clients` cash_balance and count of target salesdashboard
    :param client: client, who buy some asset
    :param deal: target salesdasboard
    :param count: count of asset, which buy client
    :param value: value of asset in target salesdasboard
    """
    broker = deal.broker
    _broker_sale_asset(broker, deal, count, value)
    _client_buy_asset(client, deal, count, value)
    deal.count -= count
    deal.save()
    if deal.count == decimal.Decimal("0"):
        deal_id = deal.id
        asset_name = deal.asset.name
        SalesDashboard.objects.filter(id=deal_id).delete()
        transaction.on_commit(
            lambda: notify.s(
                notification_type=NotificationType.SALESDASHBOARD_IS_OVER,
                account_id=broker.id,
                deal_id=deal_id,
                asset_name=asset_name,
            ).apply_async(task_id=f"salesdashboard_is_over notification: {deal_id}")
        )


@transaction.atomic
def offer_flow(offer_count, client, deal) -> dict:
    """
    Validate request data, create and serialize new object of Offer
    Notify broker
    """
    validators.validate_offer_count(offer_count, deal)

    offer = Offer(
        asset=deal.asset,
        broker=deal.broker,
        client=client,
        price=deal.price,
        count=offer_count,
    )
    deal_value = decimal.Decimal(offer.total_value)
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)

    offer_notifications_for_broker(offer, deal)
    return serializer.data


def offer_notifications_for_broker(offer, deal):
    breakpoint()
    if deal.success_offer_notification:
        transaction.on_commit(
            lambda: notify.s(
                notification_type=NotificationType.SUCCESS_OFFER,
                account_id=offer.broker.id,
                offer_id=offer.id,
            ).apply_async(task_id=f"offer_success notification: {offer.id}")
        )
    if deal.count < deal.count_control_notification:
        transaction.on_commit(
            lambda: notify.s(
                notification_type=NotificationType.SALESDASHBOARD_SOON_OVER,
                account_id=offer.broker.id,
                salesdashboard_id=deal.id,
            ).apply_async(task_id=f"salesdashboard soon_over notification: {deal.id}")
        )


def _get_offers(request):
    if request.auth["user_role"] == "client":
        return Offer.objects.filter(client_id=request.user.account.client.id)
    elif request.auth["user_role"] == "broker":
        return Offer.objects.filter(broker__id=request.user.account.broker.id)


def get_offers_with_related_items(request):
    return (
        _get_offers(request)
        .prefetch_related("asset__wallet_record")
        .select_related(
            "asset",
            "broker__owner",
            "broker__wallet",
            "client__owner",
            "client__wallet",
        )
        .all()
        .order_by("id")
    )


def purchase_asset(broker, market, asset_name, count):
    get_validated_asset_from_market(asset_name, market)
    deal = market.client.buy(name=asset_name, count=count)
    validate_broker_cash_balance(broker.cash_balance, deal["total_price"])
    asset, created = Asset.objects.get_or_create(
        name=deal["asset"]["name"], description=deal["asset"]["description"]
    )

    purchase = PurchaseDashboard.objects.create(
        asset=asset,
        market=market,
        broker=broker,
        count=deal["count"],
        price=deal["asset"]["price"],
    )

    _update_broker_account_after_purchase(
        purchase.asset, broker, purchase.count, deal["total_price"]
    )
    return deal


@transaction.atomic
def _update_broker_account_after_purchase(asset, broker, count, deal_total_price):
    broker_wallet_record, created = WalletRecord.objects.get_or_create(
        asset=asset, wallet=broker.wallet
    )
    broker_wallet_record.count += count
    broker_wallet_record.save()
    broker.cash_balance -= deal_total_price
    broker.save()


def get_purchasedashboards_with_related_items(request):
    return (
        PurchaseDashboard.objects.filter(broker=request.user.account.broker)
        .select_related("broker__owner", "broker__wallet", "asset", "market")
        .order_by("id")
    )

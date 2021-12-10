import decimal

from account.models import Offer, PurchaseDashboard, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from asset.models import Asset
from django.db import transaction
from utils import validators
from utils.validators import validate_broker_cash_balance
from wallet.models import WalletRecord


def create_sale_object_serializer(count, price, asset, request) -> dict:
    """
    Validate request, create and serialize new object of SalesDashboard
    """
    validators.validate_is_broker(request)
    broker = request.user.account.broker
    validators.validate_asset_exists(asset, broker)
    validators.validate_asset_count(count, asset, broker)

    new_object = SalesDashboard.objects.create(
        asset=asset, broker=broker, count=count, price=price
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


def _update_deal(deal, count):
    deal.count -= count
    deal.save()


def deal_flow(client, deal, count, value):
    broker = deal.broker
    _broker_sale_asset(broker, deal, count, value)
    _client_buy_asset(client, deal, count, value)
    _update_deal(deal, count)


def offer_flow(offer_count, request, deal) -> dict:
    """
    Validate request, create and serialize new object of Offer
    """
    validators.validate_is_client(request)
    validators.validate_offer_count(offer_count, deal)

    client = request.user.account.client
    offer = Offer(deal=deal, client=client, count=offer_count)
    deal_value = decimal.Decimal(offer.total_value)
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)
    return serializer.data


def _get_offers(request):
    if request.auth["user_role"] == "client":
        return Offer.objects.filter(client_id=request.user.account.client.id)
    elif request.auth["user_role"] == "broker":
        return Offer.objects.filter(deal__broker__id=request.user.account.broker.id)


def get_offers_with_related_items(request):
    return (
        _get_offers(request)
        .prefetch_related("deal__asset__wallet_record")
        .select_related(
            "deal__asset",
            "deal__broker__owner",
            "deal__broker__wallet",
            "client__owner",
            "client__wallet",
        )
        .all()
        .order_by("id")
    )


def purchase_asset(request, market, asset_name, count):
    deal = market.client.buy(name=asset_name, count=count)
    validate_broker_cash_balance(
        request.user.account.broker.cash_balance, deal["total_price"]
    )

    Asset.objects.get_or_create(
        name=deal["asset"]["name"], description=deal["asset"]["description"]
    )

    purchase = PurchaseDashboard.objects.create(
        asset=Asset.objects.get(name=deal["asset"]["name"]),
        market=market,
        broker=request.user.account.broker,
        count=deal["count"],
        price=deal["asset"]["price"],
    )

    _update_broker_account_after_purchase(
        purchase.asset, request.user.account.broker, purchase.count, deal["total_price"]
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

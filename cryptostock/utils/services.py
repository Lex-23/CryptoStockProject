import decimal

from account.models import Offer, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from utils import validators
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
    broker_wallet_record.count -= decimal.Decimal(count)
    broker_wallet_record.save()
    broker.cash_balance += decimal.Decimal(value)
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
        client_wallet_record.count += decimal.Decimal(count)
        client_wallet_record.save()
    else:
        WalletRecord.objects.create(asset=deal.asset, wallet=client.wallet, count=count)
    client.cash_balance -= decimal.Decimal(value)
    client.save()


def _update_deal(deal, count):
    deal.count -= decimal.Decimal(count)
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
    deal_value = offer.total_value
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)
    return serializer.data

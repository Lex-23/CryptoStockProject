import decimal

from account.models import Offer, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from utils import validators


def create_sale_object(serializer, asset, request):
    broker = request.user.account.broker

    validators.validate_is_broker(request)
    validators.validate_asset_exists(asset, broker)
    validators.validate_asset_count(request, asset, broker)

    new_object = SalesDashboard.objects.create(
        asset=asset,
        broker=broker,
        count=serializer.data["count"],
        price=serializer.data["price"],
    )
    serializer_data = SalesDashboardSerializer(new_object).data
    return serializer_data


def _broker_sale_asset(broker, deal, count, value):
    broker_wallet_record = broker.wallet.wallet_record.get(asset=deal.asset)
    broker_wallet_record.count -= decimal.Decimal(count)
    broker_wallet_record.save()
    broker.cash_balance += decimal.Decimal(value)
    broker.save()


def _asset_exists_in_wallet(deal, client):
    asset = deal.asset
    return client.wallet.wallet_record.filter(asset=asset).exists()


def _client_buy_asset(client, deal, count, value):
    if _asset_exists_in_wallet(deal, client):
        client_wallet_record = client.wallet.wallet_record.get(asset=deal.asset)
        client_wallet_record.count += decimal.Decimal(count)
        client_wallet_record.save()
    else:
        client.wallet.wallet_record.create(asset=deal.asset, count=count)
    client.cash_balance -= decimal.Decimal(value)
    client.save()


def create_offer(client, deal, count):
    offer = Offer(deal=deal, client=client, count=count)
    return offer


def _update_deal(deal, count):
    deal.count -= decimal.Decimal(count)
    deal.save()


def deal_flow(client, deal, count, value):
    broker = deal.broker
    _broker_sale_asset(broker, deal, count, value)
    _client_buy_asset(client, deal, count, value)
    _update_deal(deal, count)


def offer_flow(serializer, request, deal):
    client = request.user.account.client
    offer_count = serializer.data["count"]

    validators.validate_is_client(request)
    validators.validate_offer_count(serializer, deal)

    offer = create_offer(client, deal, offer_count)
    deal_value = offer.total_value
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)
    return serializer.data

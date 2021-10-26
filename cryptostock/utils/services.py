import decimal

from account.models import Offer, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from django.http import Http404
from utils import validators
from wallet.models import WalletRecord


def create_sale_object_serializer(count, price, asset, request):
    account = request.user.account
    validators.validate_is_broker(account)
    broker = account.broker
    validators.validate_asset_exists(asset, broker)
    data = request.data
    validators.validate_asset_count(data, asset, broker)

    new_object = SalesDashboard.objects.create(
        asset=asset, broker=broker, count=count, price=price
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
        WalletRecord.objects.create(asset=deal.asset, wallet=client.wallet, count=count)
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


def offer_flow(offer_count, request, deal):
    account = request.user.account
    validators.validate_is_client(account)
    validators.validate_offer_count(offer_count, deal)

    client = account.client
    offer = create_offer(client, deal, offer_count)
    deal_value = offer.total_value
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)
    return serializer.data


def get_object(pk, snippet):
    try:
        return snippet.objects.get(pk=pk)
    except snippet.DoesNotExist:
        raise Http404

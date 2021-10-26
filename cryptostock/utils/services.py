import decimal

from account.models import Offer, SalesDashboard
from account.serializers import OfferSerializer, SalesDashboardSerializer
from django.http import Http404
from utils import validators
from wallet.models import WalletRecord


def create_sale_object_serializer(count, price, asset, request) -> dict:
    """
    Validate request, create and serialize new object of SalesDashboard
    :param count: asset count for new sale
    :param price: asset price for new sale
    :param asset: target asset object
    :param request:
    :return: serializer(new_sale).data
    """
    validators.validate_is_broker(request.user.account)
    broker = request.user.account.broker
    validators.validate_asset_exists(asset, broker)
    data = request.data
    validators.validate_asset_count(data, asset, broker)

    new_object = SalesDashboard.objects.create(
        asset=asset, broker=broker, count=count, price=price
    )
    serializer_data = SalesDashboardSerializer(new_object).data
    return serializer_data


def _broker_sale_asset(broker, deal, count, value):
    """
    Update broker`s cash_balance and wallet_record after offer
    :param broker: broker object
    :param deal: target sale
    :param count: offer count
    :param value: offer value
    :return: None
    """
    broker_wallet_record = broker.wallet.wallet_record.get(asset=deal.asset)
    broker_wallet_record.count -= decimal.Decimal(count)
    broker_wallet_record.save()
    broker.cash_balance += decimal.Decimal(value)
    broker.save()


def _asset_exists_in_wallet(deal, client):
    """
    Check exists asset from target sale in client`s wallet
    :param deal: target sale
    :param client: client object
    :return: bool
    """
    asset = deal.asset
    return client.wallet.wallet_record.filter(asset=asset).exists()


def _client_buy_asset(client, deal, count, value):
    """
    Update clients`s cash_balance and wallet_record after offer
    :param client: client object
    :param deal: target sale
    :param count: offer count
    :param value: offer value
    :return: None
    """
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


def offer_flow(offer_count, request, deal) -> dict:
    """
    Validate request, create and serialize new object of Offer
    :param offer_count: count for offer
    :param request:
    :param deal: target sale
    :return: serializer(new_offer).data
    """
    validators.validate_is_client(request.user.account)
    validators.validate_offer_count(offer_count, deal)

    client = request.user.account.client
    offer = create_offer(client, deal, offer_count)
    deal_value = offer.total_value
    validators.validate_cash_balance(client, deal_value)

    deal_flow(client, deal, offer_count, deal_value)
    offer.save()
    serializer = OfferSerializer(offer)
    return serializer.data


def get_object(snippet, pk):
    try:
        return snippet.objects.get(pk=pk)
    except snippet.DoesNotExist:
        raise Http404

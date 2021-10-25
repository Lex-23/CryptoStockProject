import decimal

from account.models import Offer, SalesDashboard
from account.serializers import SalesDashboardSerializer


def create_sale_object(serializer, asset, broker):
    new_object = SalesDashboard.objects.create(
        asset=asset,
        broker=broker,
        count=serializer.data["count"],
        price=serializer.data["price"],
    )
    serializer_data = SalesDashboardSerializer(new_object).data
    return serializer_data


def broker_wallet_record_flow(broker, deal, count):
    broker_wallet_record = broker.wallet.wallet_record.get(asset=deal.asset)
    broker_wallet_record.count -= decimal.Decimal(count)
    broker_wallet_record.save()


def _asset_exists_in_wallet(deal, client):
    asset = deal.asset
    return client.wallet.wallet_record.filter(asset=asset).exists()


def client_wallet_record_flow(client, deal, count):
    if _asset_exists_in_wallet(deal, client):
        client_wallet_record = client.wallet.wallet_record.get(asset=deal.asset)
        client_wallet_record.count += decimal.Decimal(count)
        client_wallet_record.save()
    else:
        client.wallet.wallet_record.create(asset=deal.asset, count=count)


def create_offer(client, deal, count):
    offer = Offer(deal=deal, client=client, count=count)
    return offer

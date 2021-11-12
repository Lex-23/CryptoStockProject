import factory
from account.models import Broker, SalesDashboard
from asset.models import Asset
from factory.django import DjangoModelFactory
from wallet.models import Wallet, WalletRecord


class AssetFactory(DjangoModelFactory):
    class Meta:
        model = Asset

    name = "BTC"
    description = "asset_description"


class WalletRecordFactory(DjangoModelFactory):
    class Meta:
        model = WalletRecord

    asset = factory.SubFactory(AssetFactory)
    count = "500.0000"
    wallet = factory.SubFactory(Wallet)


class SalesDashboardFactory(DjangoModelFactory):
    class Meta:
        model = SalesDashboard

    asset = factory.SubFactory(AssetFactory)
    broker = factory.SubFactory(Broker)
    count = "50.5555"
    price = "200.777777"

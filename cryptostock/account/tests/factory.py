import factory
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
    count = 500
    wallet = factory.SubFactory(Wallet)

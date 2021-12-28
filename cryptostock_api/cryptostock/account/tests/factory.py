import decimal

import factory
from account.models import Broker, Client, Offer, PurchaseDashboard, SalesDashboard
from asset.models import Asset
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from market.tests.factory import MarketFactory
from wallet.models import Wallet, WalletRecord


class AssetFactory(DjangoModelFactory):
    class Meta:
        model = Asset

    name = factory.Sequence(lambda n: f"asset#{n:03}")
    description = "asset_description"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user#{n:03}")


class WalletFactory(DjangoModelFactory):
    class Meta:
        model = Wallet

    name = "Wallet name"


class WalletRecordFactory(DjangoModelFactory):
    class Meta:
        model = WalletRecord

    asset = factory.SubFactory(AssetFactory)
    count = "500.0000"
    wallet = factory.SubFactory(WalletFactory)


class BrokerFactory(DjangoModelFactory):
    class Meta:
        model = Broker

    owner = factory.SubFactory(UserFactory)
    name = "Another broker"
    wallet = factory.SubFactory(WalletFactory)


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    owner = factory.SubFactory(UserFactory)
    name = "Another client"
    wallet = factory.SubFactory(WalletFactory)


class SalesDashboardFactory(DjangoModelFactory):
    class Meta:
        model = SalesDashboard

    asset = factory.SubFactory(AssetFactory)
    broker = factory.SubFactory(BrokerFactory)
    count = decimal.Decimal("50.5555")
    price = decimal.Decimal("200.77")


class OfferFactory(DjangoModelFactory):
    class Meta:
        model = Offer

    deal = factory.SubFactory(SalesDashboardFactory)
    client = factory.SubFactory(ClientFactory)
    count = decimal.Decimal("10.5555")


class PurchaseDashboardFactory(DjangoModelFactory):
    class Meta:
        model = PurchaseDashboard

    asset = factory.SubFactory(AssetFactory)
    broker = factory.SubFactory(BrokerFactory)
    market = factory.SubFactory(MarketFactory)
    price = decimal.Decimal("5.55")
    count = decimal.Decimal("10.0000")

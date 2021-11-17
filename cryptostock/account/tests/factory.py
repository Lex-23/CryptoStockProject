import decimal

import factory
from account.models import Broker, Client, Offer, SalesDashboard
from asset.models import Asset
from django.contrib.auth.models import User
from factory import Faker
from factory.django import DjangoModelFactory
from wallet.models import Wallet, WalletRecord


class AssetFactory(DjangoModelFactory):
    class Meta:
        model = Asset

    name = "BTC"
    description = "asset_description"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("first_name")


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
    price = decimal.Decimal("200.777777")


class OfferFactory(DjangoModelFactory):
    class Meta:
        model = Offer

    deal = factory.SubFactory(SalesDashboardFactory)
    client = factory.SubFactory(ClientFactory)
    count = decimal.Decimal("10.5555")

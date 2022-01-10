import factory
from account.models import Account
from account.tests.factory import UserFactory, WalletFactory
from factory.django import DjangoModelFactory
from notification.models import Consumer, NotificationSubscription


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    owner = factory.SubFactory(UserFactory)
    name = "Random Account"
    wallet = factory.SubFactory(WalletFactory)


class ConsumerFactory(DjangoModelFactory):
    class Meta:
        model = Consumer

    account = factory.SubFactory(AccountFactory)


class NotificationSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = NotificationSubscription

    account = factory.SubFactory(AccountFactory)

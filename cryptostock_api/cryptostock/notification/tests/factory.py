import factory
from account.models import Account
from account.tests.factory import UserFactory, WalletFactory
from factory.django import DjangoModelFactory
from notification.models import Consumer, NotificationSubscription


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    owner = factory.SubFactory(UserFactory)
    name = "Account name"
    wallet = factory.SubFactory(WalletFactory)


class ConsumerFactory(DjangoModelFactory):
    class Meta:
        model = Consumer


class NotificationSubscriptionFactory(DjangoModelFactory):
    account = factory.SubFactory(AccountFactory)

    class Meta:
        model = NotificationSubscription

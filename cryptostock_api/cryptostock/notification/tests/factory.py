from factory.django import DjangoModelFactory
from notification.models import Consumer, NotificationSubscription


class ConsumerFactory(DjangoModelFactory):
    class Meta:
        model = Consumer


class NotificationSubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = NotificationSubscription

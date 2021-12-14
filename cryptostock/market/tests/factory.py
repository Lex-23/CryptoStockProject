import factory
from factory.django import DjangoModelFactory
from market.models import Market


class MarketFactory(DjangoModelFactory):
    class Meta:
        model = Market

    name = factory.Sequence(lambda n: f"market#{n:03}")
    url = factory.Sequence(lambda n: f"http://{n:03}")

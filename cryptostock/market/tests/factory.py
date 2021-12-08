from factory.django import DjangoModelFactory
from market.models import Market


class MarketFactory(DjangoModelFactory):
    class Meta:
        model = Market

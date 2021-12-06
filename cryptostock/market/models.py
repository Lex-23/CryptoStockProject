import abc
from typing import Dict, List

from django.db import models
from market.helpers import _yahoo_scraper


class AbstractMarket(abc.ABC):
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_assets(self) -> List[Dict]:
        """Return all allowed assets from market"""

    @abc.abstractmethod
    def get_asset(self, name) -> Dict:
        """ Return asset by name"""

    @abc.abstractmethod
    def buy(self, name, count) -> Dict:
        """ Buy asset by name"""


_market_storage = {}


def market_register(cls):
    _market_storage[cls.NAME] = cls
    return cls


@market_register
class YahooMarket(AbstractMarket):
    NAME = "Yahoo"

    def get_assets(self):
        return _yahoo_scraper(url=self.url)

    def get_asset(self, name) -> Dict:
        asset = [i for i in self.get_assets() if i["name"] == name][0]
        return asset

    def buy(self, name, count) -> Dict:
        return {"asset": self.get_asset(name), "count": count}


class Market(models.Model):
    name = models.CharField(max_length=20, unique=True)
    url = models.URLField()
    kwargs = models.JSONField(default=dict)

    @property
    def market_cls(self):
        market_cls = _market_storage.get(self.name)
        if market_cls is None:
            raise ValueError(f"Market with name {self.name} doesn't exist")
        return market_cls

    @property
    def client(self):
        kwargs = self.kwargs
        return self.market_cls(url=self.url, **kwargs)

    def __str__(self):
        return self.name

from typing import Dict, List

from django.db import models
from utils.scraper import yahoo_scraper


class AbstractMarket:
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

    def get_assets(self) -> List[Dict]:
        pass

    def get_asset(self, name) -> Dict:
        asset = [i for i in self.get_assets() if i["name"] == name][0]
        return asset

    def buy(self, name, count) -> Dict:
        return {"asset": self.get_asset(name), "count": count}


_market_storage = {}


def market_register(cls):
    _market_storage[cls.NAME] = cls
    return cls


@market_register
class YahooMarket(AbstractMarket):
    NAME = "Yahoo"

    def get_assets(self):
        return yahoo_scraper(url=self.url)


class Market(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()
    kwargs = models.JSONField(blank=True, null=True)

    @property
    def market_cls(self):
        market_cls = _market_storage.get(self.name)
        if market_cls is None:
            raise ValueError(f"Market with name {self.name} doesn't exist")
        return market_cls

    @property
    def client(self):
        return self.market_cls(url=self.url)

    def __str__(self):
        return self.name

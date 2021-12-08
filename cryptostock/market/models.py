import abc
from functools import lru_cache
from typing import List, TypedDict

import requests
from bs4 import BeautifulSoup
from django.db import models


class Asset(TypedDict):
    name: str
    description: str
    price: str


class BuyResponse(TypedDict):
    asset: Asset
    count: int


class AbstractMarket(abc.ABC):
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs

    @abc.abstractmethod
    def get_assets(self) -> List[Asset]:
        """ Return all allowed assets from market """

    @abc.abstractmethod
    def get_asset(self, name: str) -> Asset:
        """ Return asset by name """

    @abc.abstractmethod
    def buy(self, name: str, count: int) -> BuyResponse:
        """ Buy asset by name """


_market_storage = {}


def market_register(cls):
    _market_storage[cls.NAME] = cls
    return cls


@market_register
class YahooMarket(AbstractMarket):
    NAME = "Yahoo"

    def get_assets(self):
        return self.get_assets_from_yahoo()

    def get_asset(self, name):
        asset = [asset for asset in self.get_assets() if asset["name"] == name][0]
        return asset

    def buy(self, name, count):
        return {"asset": self.get_asset(name), "count": count}

    @lru_cache(maxsize=None)
    def get_assets_from_yahoo(self):
        """
        Function for get assets info from Yahoo.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        parse_names = soup.find_all("td", attrs={"aria-label": "Symbol"})
        parse_descriptions = soup.find_all("td", attrs={"aria-label": "Name"})
        parse_price = soup.find_all("td", attrs={"aria-label": "Price (Intraday)"})

        assets_list = []
        for name, desc, price in zip(parse_names, parse_descriptions, parse_price):
            asset = {
                "name": name.text.split("-")[0],
                "description": desc.text.split()[0],
                "price": price.text.replace(",", ""),
            }
            assets_list.append(asset)
        return assets_list


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
        return self.market_cls(url=self.url, **self.kwargs)

    def __str__(self):
        return self.name

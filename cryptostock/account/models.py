from asset.models import Asset
from django.contrib.auth.models import User
from django.db import models
from utils.modules import CountField, PriceField
from wallet.models import Wallet


class Account(models.Model):
    """Base model"""

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    name = models.CharField(max_length=50)
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name="account"
    )
    cash_balance = CountField(default=0)

    def __str__(self):
        return f"{self.name} ({self.owner})"


class Broker(Account):
    pass


class Client(Account):
    pass


class SalesDashboard(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    count = CountField()
    price = PriceField()
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.asset} - price:{self.price} - broker:{self.broker}"


class Offer(models.Model):
    deal = models.ForeignKey(
        SalesDashboard, on_delete=models.CASCADE, related_name="offer"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    count = CountField()
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        return self.deal.price

    @property
    def asset(self):
        return self.deal.asset

    @property
    def broker(self):
        return self.deal.broker

    @property
    def total_value(self):
        return self.count * self.price

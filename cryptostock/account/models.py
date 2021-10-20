from asset.models import Asset
from django.contrib.auth.models import User
from django.db import models
from utils.modules import CountField
from wallet.models import Wallet


class Account(models.Model):
    """Base model"""

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    name = models.CharField(max_length=50)
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name="account"
    )

    def __str__(self):
        return f"{self.name} by {self.owner}"

    @property
    def have_assets(self):
        return list(self.wallet.all_assets)


class Broker(Account):
    pass


class Client(Account):
    pass


class AssetBuy(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    buy_count = CountField()
    timestamp = models.DateTimeField(auto_now=True)
